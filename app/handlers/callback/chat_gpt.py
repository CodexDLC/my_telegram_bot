import logging
log = logging.getLogger(__name__)

from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.types import Message


from app.resources.assets.states import ChatGpt
from app.resources.keyboards.inline import chat_inline_kb, start_inline_kb
from app.resources.text.anonce import start_text, chat_gpt_active
from app.services.chat_gpt_service import gpt_answer




router  = Router(name="chat_gpt")


@router.callback_query(F.data == "ui_chatgpt")
async def chat_gpt_handler(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await state.set_state(ChatGpt.TEXT_MSG)
    await call.message.edit_text(chat_gpt_active, parse_mode="HTML", reply_markup=chat_inline_kb())



@router.message(StateFilter(ChatGpt.TEXT_MSG), F.text)
async def fsm_text_gpt_handler(m: Message, state: FSMContext):
    if not m.text:
        await m.answer("Нужен обычный текст.")
        return
    chat_text = m.text
    msg = await m.answer("ChatGPT думает .... ")
    response = await gpt_answer("chat", chat_text)
    await msg.edit_text(response, reply_markup=chat_inline_kb())



@router.callback_query(F.data == "🔙 Вернуться в меню")
async def cancel_chatgpt_handler(call: CallbackQuery, state: FSMContext, msg=None):
    await msg.edit_text(start_text, parse_mode="HTML", reply_markup=start_inline_kb())
    await state.clear()
    """
    await call.message.edit_text(start_text, parse_mode="HTML", reply_markup=start_inline_kb()) 
    прикольное поведение можно вернуться к последнему по сути каллбеку все новые сообщение временно скроются
    и можно запустить их удаления в фоне например. 
    
    """
