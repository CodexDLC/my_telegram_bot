#app/handlers/footer_menu.py
import logging

from aiogram import F, Router
from aiogram.types import Message

from app.resources.keyboards.inline import start_inline_kb
from app.resources.keyboards.reply import (
    btn_footer_help,
    btn_footer_menu,
    btn_footer_setting,
)
from app.resources.text.anonce import setting_text, start_text
from app.resources.text.help import help_text

log = logging.getLogger(__name__)

router = Router()


@router.message(F.text == btn_footer_menu)
async def footer_menu_handler(m: Message)-> None:
    log.info(f"Поймали сообщение {btn_footer_menu}")
    await m.answer(start_text, parse_mode="HTML", reply_markup=start_inline_kb())


@router.message(F.text == btn_footer_help)
async def footer_menu_help_handler(m: Message)-> None:
    log.info(f"Поймали сообщение {btn_footer_help}")
    await m.answer(help_text, parse_mode="HTML", reply_markup=None)


@router.message(F.text == btn_footer_setting)
async def footer_menu_settings_handler(m: Message)-> None:
    log.info(f"Поймали сообщение {btn_footer_setting}")
    await m.answer(setting_text, parse_mode="HTML", reply_markup=None)