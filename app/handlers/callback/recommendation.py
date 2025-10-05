#app/handlers/callback/recommendation.py
import logging

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message


from app.resources.assets.recommen_dict import RECO_CATEGORIES
from app.resources.assets.states import Recommendations
from app.resources.keyboards.inline import recommend_inline_kb, genre_inline_kb, confirm_reco_inline_kb

from app.services.llm_provider import get_llm_answer
gpt_answer = get_llm_answer()

from app.services.recommendation_service import parser_recommendation

log = logging.getLogger(__name__)

router = Router(name="recommendation")


@router.callback_query(F.data == "reco_open")
async def recommendation_handler(call: CallbackQuery, state : FSMContext)-> None:
    await call.answer(category="", apply=[])
    await state.set_state(Recommendations.CHOOSE_CATEGORY)
    await state.update_data()
    if isinstance(call.message, Message):
        await call.message.edit_text("Выберите категорию поиска",
                                  reply_markup=recommend_inline_kb())


@router.callback_query(F.data.startswith("reco_category:"))
async def reco_category_handler(call: CallbackQuery, state: FSMContext)-> None:
    await call.answer()
    await state.set_state(Recommendations.CHOOSE_GENRE)
    apply = set()

    call_data = call.data

    text_genre = "Выбрано жанров: "
    if call_data is not None:
        category = call_data.split(":")[-1]
    else:
        category = ""

    kb = genre_inline_kb(category, apply)

    await state.update_data(category=category, apply=list(apply), text_genre=text_genre, apply_label=[])
    if isinstance(call.message, Message):
        await call.message.edit_text(text_genre,
                                  reply_markup=kb)


@router.callback_query(F.data.startswith("genre:"))
async def reco_category_apply_handler(call: CallbackQuery, state: FSMContext)-> None:
    await call.answer()

    state_data = await state.get_data()
    text_genre: str = state_data.get("text_genre") or ""
    category: str = state_data.get("category") or ""
    dict_category: dict[str, str] = RECO_CATEGORIES.get(category)
    apply  = set(state_data.get("apply"))
    apply_label = state_data.get("apply_label") or []
    call_data = call.data
    if call_data is not None:
        genre = call_data.split(":")[-1]
        log.info(f"Выбранный жанр: {genre}")
    else:
        genre = ""

    apply_label.append(dict_category.get(genre))

    apply.add(genre)
    kb = genre_inline_kb(category, apply)

    await state.update_data(apply=list(apply))

    await state.update_data(apply=list(apply), apply_label=apply_label)

    if isinstance(call.message, Message):
        str_label = ", ".join(apply_label)
        await call.message.edit_text(f"{text_genre} {str_label}",
                                  reply_markup=kb)


@router.callback_query(F.data.startswith("reco:"))
async def confirm_reco_handler(call: CallbackQuery, state: FSMContext)-> None:
    await state.set_state(Recommendations.SHOW_RECOMMENDATION)
    state_data = await state.get_data()
    apply_label = state_data.get("apply_label") or []
    exceptions = state_data.get("exceptions") or []
    category = state_data.get("category")

    call_data = call.data
    if call_data is not None:
        reco = call_data.split(":")[-1]
        log.info(f"Выбранный жанр: {reco}")
    else:
        reco = ""

    if reco == "confirm":
        resp = await gpt_answer(mode="reco", user_text="", apply_label=apply_label, category=category)
    elif reco == "restart":
        resp = await gpt_answer(mode="reco", user_text="", apply_label=apply_label, category=category, exceptions=exceptions)
    else:
        resp = ""
        log.warning(f"такого запроса нету")

    title, description, rating = await parser_recommendation(resp)
    log.info(f"Название = {title},\n Описание = {description},\n), рейтинг = {rating}")

    rating_m = ", ".join(rating)
    msg = f"""
    <b>Название: "{title}"</b>

    <i>{description}</i> 
    
    {rating_m}
    """

    if isinstance(call.message, Message):
        await call.message.edit_text(msg, parse_mode="HTML", reply_markup=confirm_reco_inline_kb())

    exceptions.append(title)
    await state.update_data(exceptions=exceptions)


