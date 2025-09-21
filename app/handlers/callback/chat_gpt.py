import logging

from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from pyexpat.errors import messages

log = logging.getLogger(__name__)

from aiogram import F, Router




router  = Router(name="chat_gpt")




@router.callback_query(F.data == "ui_chatgpt")
async def chat_gpt_handler(call: CallbackQuery, state: FSMContext):
    await call.message.answer("")
    pass

