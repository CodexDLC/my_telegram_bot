# app/handlers/callback/universal.py
import logging

from aiogram import F, Router
from aiogram.types import CallbackQuery, Message

from app.resources.keyboards.inline import start_inline_kb
from app.resources.text.anonce import start_text

log = logging.getLogger(__name__)

router = Router()

main_menu = "main_menu"


@router.callback_query(F.data == main_menu)
async def main_menu_handler(call: CallbackQuery)-> None:
    log.info("Поймали сообщение маин меню")
    if isinstance(call.message, Message):
        await call.message.edit_text(
            start_text, parse_mode="HTML", reply_markup=start_inline_kb()
        )
