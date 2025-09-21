import logging

from app.resources.keyboards.inline import start_inline_kb
from app.resources.keyboards.reply import btn_footer_menu, btn_footer_help, btn_footer_setting
from app.resources.text.anonce import start_text, setting_text
from app.resources.text.help import help_text

log = logging.getLogger(__name__)

from aiogram import Router, F

from aiogram.types import Message


router = Router()


@router.message(F.text == btn_footer_menu)
async def footer_menu_handler(m: Message):
    log.info(f"Поймали сообщение {btn_footer_menu}")
    await m.answer(start_text,parse_mode="HTML",reply_markup=start_inline_kb())


@router.message(F.text == btn_footer_help)
async def footer_menu_handler(m: Message):
    log.info(f"Поймали сообщение {btn_footer_help}")
    await m.answer(help_text, parse_mode="HTML",reply_markup=None)


@router.message(F.text == btn_footer_setting)
async def footer_menu_handler(m: Message):
    log.info(f"Поймали сообщение {btn_footer_setting}")
    await m.answer(setting_text, parse_mode="HTML",reply_markup=None)