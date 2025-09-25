#app/handlers/callback/chat_gpt.py
import logging
from keyword import kwlist

from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from app.handlers.callback.constant import MAX_LEN, gpt_role, mod_chat_gpt
from app.resources.assets.states import ChatGpt
from app.resources.keyboards.inline import chat_inline_kb, start_inline_kb
from app.resources.text.anonce import chat_gpt_active, start_text
from app.services.chat_gpt_service import gpt_answer
from app.services.context_service import get_history, add_message

log = logging.getLogger(__name__)

router = Router(name="chat_gpt")


@router.callback_query(F.data == "ui_chatgpt")
async def chat_gpt_handler(call: CallbackQuery, state: FSMContext)-> None:
    await call.answer()
    await state.set_state(ChatGpt.TEXT_MSG)
    if isinstance(call.message, Message):
        await call.message.edit_text(
            chat_gpt_active, parse_mode="HTML", reply_markup=chat_inline_kb()
        )


@router.message(StateFilter(ChatGpt.TEXT_MSG), F.text)
async def fsm_text_gpt_handler(m: Message, state: FSMContext)-> None:

    if not m.text:
        await m.answer("Нужен обычный текст.")
    elif len(m.text) > MAX_LEN:
        await m.answer(
            f"Нужен текст до {MAX_LEN} символов вы отправили {len(m.text)} символов."
        )
        return
    user_id = m.from_user.id
    await add_message(user_id, mod_chat_gpt, "user", m.text)

    chat_text = f"{m.text}"
    histore_context = await get_history(user_id, mod_chat_gpt)
    msg = await m.answer("ChatGPT думает .... ")

    response = await gpt_answer("chat", user_text=chat_text, history=histore_context)
    await add_message(user_id, mod_chat_gpt, gpt_role, response)

    await msg.edit_text(response, reply_markup=chat_inline_kb())


@router.callback_query(F.data == "🔙 Вернуться в меню")
async def cancel_chatgpt_handler(call: CallbackQuery, state: FSMContext)-> None:
    if isinstance(call.message, Message):
        await call.message.edit_text(start_text, parse_mode="HTML", reply_markup=start_inline_kb())
    await state.clear()
    """
    await call.message.edit_text(start_text, parse_mode="HTML", reply_markup=start_inline_kb()) 
    прикольное поведение можно вернуться к последнему по сути каллбеку все новые сообщение временно скроются
    и можно запустить их удаления в фоне например. 
    
    """
