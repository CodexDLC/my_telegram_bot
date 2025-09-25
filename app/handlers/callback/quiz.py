# app/handlers/callback/quiz.py
import logging

from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from app.handlers.callback.constant import gpt_role
from app.resources.assets.quiz_theme import ALL_DIFFICULTIES, DIFFICULTY_DATA, QUIZ_THEME, TOPIC_KEYS
from app.resources.assets.states import QuizGame
from app.resources.keyboards.inline import get_theme_quiz_inline_kb, star_game_inline_kb
from app.services.chat_gpt_service import gpt_answer
from app.services.context_service import add_message, get_history
from app.services.quiz_service import make_ui_quiz, parser_question, summ_score

log = logging.getLogger(__name__)

router = Router(name="quiz_chat")


@router.callback_query(F.data == "quiz_open")
async def quiz_start_handler(call: CallbackQuery, state: FSMContext)-> None:
    await state.set_state(QuizGame.START_GAME)
    if isinstance(call.message, Message):
        await call.message.edit_text("Выберите тему для игры", reply_markup=get_theme_quiz_inline_kb())


@router.callback_query(StateFilter(QuizGame.START_GAME), F.data.startswith("theme:"))
async def pick_theme_handler(call: CallbackQuery, state: FSMContext)-> None:

    data = call.data

    if not data:
        await call.answer("Пустой callback", show_alert=False)
        return

    topic: str = data.strip(":")[-1]
    if not topic:
        await call.answer("Некорректный callback", show_alert=True)
        return

    if topic not in TOPIC_KEYS:
        # тут m может быть Inaccessible/None — если нужно, добавь проверку isinstance, см. ниже
        await call.answer("Такая тема сейчас не доступна")
        return

    theme = QUIZ_THEME[topic]
    difficulty = ALL_DIFFICULTIES[0]
    log.info("{theme}")
    score_game = 0
    score_round = 0
    right_ans = 0
    miss_ans = 0
    await state.update_data(topic=topic, difficulty=difficulty,score_round=score_round,
                            score_game=score_game, label=DIFFICULTY_DATA["easy"]["label"],
                            right_ans=right_ans, miss_ans=miss_ans)

    state_data = await state.get_data()

    text_ui = make_ui_quiz(state_data)
    if isinstance(call.message, Message):
        await call.message.edit_text(f"{text_ui} {theme["descriptions"]} ",
                                 parse_mode="HTML", reply_markup=star_game_inline_kb())
    await state.set_state(QuizGame.PLAYING_GAME)


@router.callback_query(StateFilter(QuizGame.PLAYING_GAME), F.data.startswith("game:"))
async def quiz_question_handler(call: CallbackQuery, state: FSMContext) -> None:

    data = await state.get_data()
    topic = data.get("topic")
    score_round = data["score_round"]
    score_game = data["score_game"]
    difficulty = data["difficulty"]
    user_id = call.from_user.id
    mode_context = "quiz_quest_history"

    log.debug(f"\ntopic = {topic}\n difficulty = {difficulty}\n"
              f"score_game = {score_game}\n score_round = {score_round}\n"
              f"label = {data["label"]}")

    if call.data == "game:start":
        context = await get_history(user_id, mode_context)
        resp_question = await gpt_answer("quiz", "", difficulty=difficulty, topic=topic, context=context)
        log.debug(f"{resp_question}")
        text_quest, in_res, res_text, clearn_question, kb = await parser_question(resp_question)
        await add_message(user_id, mode_context, gpt_role, clearn_question)
        await state.update_data(in_res=in_res, res_text=res_text, text_quest=text_quest)
        ui_game = make_ui_quiz(data)
        if isinstance(call.message, Message):
            await call.message.edit_text(f"{ui_game} {text_quest}", parse_mode="HTML", reply_markup=kb)



    elif call.data == "game:finish":
        await state.clear()
        if isinstance(call.message, Message):
            await state.set_state(QuizGame.START_GAME)
            await call.message.edit_text(f"Вы набрали {data["score_game"]} потратили {data["score_round"]} раундов"
                                      f"правильных ответов {data["right_ans"]}ш. "
                                      f"Не правильных ответов {data["miss_ans"]}i.",
                                      parse_mode="HTML",
                                      reply_markup=get_theme_quiz_inline_kb())


@router.callback_query(StateFilter(QuizGame.PLAYING_GAME), F.data.startswith("index:"))
async def quiz_answer_handler(call: CallbackQuery, state: FSMContext)-> None:
    data_str = call.data
    if not data_str:
        await call.answer("Пустой callback", show_alert=False)
        return

    ans_data: str = data_str.partition(":")[2]

    data = await state.get_data()
    in_res = str(data["in_res"])
    res_text = data["res_text"]
    score_game = int(data["score_game"])
    score_round = int(data["score_round"]) + 1
    label = data["label"]
    right_ans = data["right_ans"]
    miss_ans = data["miss_ans"]
    difficulty = data["difficulty"]
    log.debug(f"\n Answer_handler \nin_res = {in_res}\n res_text = {res_text}\n"
             f"score_game = {score_game}\n label = {label}\n "
              f"score_round = {score_round}" )

    thresholds = [
        (12, 30, "impossible"),
        (7, 7, "hard"),
        (3, 3, "normal"),
    ]
    for r, g, level in thresholds:
        if score_round == r and score_game >= g:
            difficulty = level
            break



    ui_game = make_ui_quiz(data)

    if in_res == ans_data:
        score_game = await summ_score(dif=difficulty,score=score_game)

        if isinstance(call.message, Message):
            await call.message.edit_text(f"{ui_game}\n Правильно! Накоплено очков {score_game}",
                                      parse_mode="HTML",
                                      reply_markup=star_game_inline_kb())
            right_ans += 1
            if score_game >= 100 and isinstance(call.message, Message):
                await call.message.edit_text(f"Вы набрали {score_game} потратили {score_round} раундов"
                                                 f"правильных ответов {right_ans}ш. Не правильных ответов {miss_ans}i.",
                                                 parse_mode="HTML",
                                                 reply_markup=get_theme_quiz_inline_kb())
    else:
        if isinstance(call.message, Message):
            await call.message.edit_text(f"{ui_game}\n правильный ответ \n{res_text}",
                                      parse_mode="HTML",
                                      reply_markup=star_game_inline_kb())
            miss_ans += 1



    log.debug(
        f"Перед новым заданием  {difficulty}"
    )

    await state.update_data(
        right_ans   = right_ans,
        miss_ans    = miss_ans,
        score_game  = score_game,
        score_round = score_round,
        difficulty  = difficulty,


    )




