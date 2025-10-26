# app/handlers/callback/translate_talk.py
import logging

from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from app.handlers.callback.constant import MAX_LEN
from app.resources.assets.states import TranslateChat
from app.resources.assets.translite_dict import lang
from app.resources.keyboards.inline import chat_inline_kb, translate_inline_kb
from app.resources.text.anonce import start_text, translate_chat
from app.services.llm_provider import get_llm_answer
from database.db import get_db_connection
from database.repositories import get_user_repo

log = logging.getLogger(__name__)

router = Router(name="translate_talk")


@router.callback_query(F.data == "translate_open")
async def translate_start_handler(call: CallbackQuery, state: FSMContext) -> None:
    to_lang = None
    log.info("Поймали translate_open")
    await call.answer()
    await state.set_state(TranslateChat.TEXT_TRANSLATE)
    data = await state.get_data()
    if "to_lang" not in data:
        to_lang = "en"
        await state.update_data(to_lang=to_lang)
        log.info(f"{data}")
    else:
        to_lang = data.get("to_lang")

    if isinstance(call.message, Message):
        await call.message.edit_text(
            translate_chat, parse_mode="HTML", reply_markup=translate_inline_kb(to_lang)
        )


@router.message(StateFilter(TranslateChat.TEXT_TRANSLATE), F.text)
async def fsm_text_gpt_handler(m: Message, state: FSMContext)-> None:
    if not m.text:
        await m.answer("Нужен обычный текст.")
    elif len(m.text) > MAX_LEN:
        await m.answer(
            f"Нужен текст до {MAX_LEN} символов вы отправили {len(m.text)} символов."
        )
        return

    data = await state.get_data()
    user_id = m.from_user.id if m.from_user else None

    async with get_db_connection() as db:
        user_repo = get_user_repo(db)
        user_row = await user_repo.get_user(user_id)

    answer_fn = get_llm_answer(user_row)
    tlang = data.get("to_lang")
    chat_text = f"Переведи этот текст на {tlang}: {m.text}"
    await m.answer("Переводим ваш текст .... ")
    response = await answer_fn("translate", chat_text)
    await m.reply(response, reply_markup=chat_inline_kb())


@router.callback_query(F.data.startswith("tlang:"))
async def set_lang(call: CallbackQuery, state: FSMContext) -> None:
    code = None
    if isinstance(call.data, str):
        code = call.data.split(":", 1)[-1]
        await state.update_data(to_lang=code)
    language = lang.get(code)
    await call.message.edit_text(f"Вы выбрали язык: {language}", reply_markup=translate_inline_kb(code))




@router.callback_query(F.data == "🔙 Вернуться в меню")
async def cancel_chatgpt_handler(call: CallbackQuery, state: FSMContext)-> None:
    log.debug("Поймали сообщение: '🔙 Вернуться в меню'")
    await state.clear()
    if isinstance(call.message, Message):
        await call.message.edit_text(
            start_text, parse_mode="HTML", reply_markup=chat_inline_kb()
        )
