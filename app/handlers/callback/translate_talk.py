import logging

from app.resources.assets.states import TranslateChat
from app.resources.keyboards.inline import chat_inline_kb, translate_inline_kb
from app.resources.text.anonce import translate_chat, start_text
from app.services.chat_gpt_service import gpt_answer

log = logging.getLogger(__name__)

from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.types import Message


router  = Router(name="translate_talk")

MAX_LEN = 2048

@router.callback_query(F.data == "translate_open")
async def translate_start_handler(call: CallbackQuery, state: FSMContext):
    log.info("Поймали translate_open")
    await call.answer()
    await state.set_state(TranslateChat.TEXT_TRANSLATE)
    log.info(f"{state}")
    data = await state.get_data()
    log.info(f"{data}")
    if "to_lang" not in data:
        to_lang = "en"
        await state.update_data(to_lang=to_lang)
        log.info(f"{data}")
    await call.message.edit_text(translate_chat, parse_mode="HTML", reply_markup=translate_inline_kb())


@router.message(StateFilter(TranslateChat.TEXT_TRANSLATE), F.text)
async def fsm_text_gpt_handler(m: Message, state: FSMContext):
    if not m.text:
        await m.answer("Нужен обычный текст.")
    elif len(m.text) > MAX_LEN:
        await m.answer(f"Нужен текст до {MAX_LEN} символов вы отправили {len(m.text)} символов.")
        return
    data = await state.get_data()
    tlang = data.get("to_lang")
    chat_text = f"Переведи этот текст на {tlang}: {m.text}"
    msg_tran = await m.answer("Переводим ваш текст .... ")
    response = await gpt_answer("translate", chat_text)
    await m.reply(response, reply_markup=chat_inline_kb())


@router.callback_query(F.data.startswith("tlang:"))
async def set_lang(call: CallbackQuery, state: FSMContext):
    code = call.data.split(":", 1)[1]
    await state.update_data(to_lang=code)
    await call.answer(f"Язык переключён на {code}")


@router.callback_query(F.data == "🔙 Вернуться в меню")
async def cancel_chatgpt_handler(call: CallbackQuery, state: FSMContext):
    log.debug("Поймали сообщение: '🔙 Вернуться в меню'")
    await state.clear()
    await call.message.edit_text(start_text, parse_mode="HTML", reply_markup=chat_inline_kb())
