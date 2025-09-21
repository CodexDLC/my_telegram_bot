import logging

log = logging.getLogger(__name__)

from aiogram import Router, F
from aiogram.types import CallbackQuery

from app.resources.keyboards.inline import start_inline_kb
from app.resources.text.anonce import start_text

router = Router()

main_menu = "main_menu"

@router.callback_query(F.data == main_menu)
async def main_menu_handler(call: CallbackQuery):
    log.info(f"Поймали сообщение маин меню")
    await call.message.edit_text(start_text,parse_mode="HTML",reply_markup=start_inline_kb())