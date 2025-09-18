# presentation/route/chat.py

from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardRemove

from constant.F_text_menu import kb_maine_help, kb_maine_hide, kb_maine_ad
from presentation.text.help import help_text
from services.handlers_command.start_menu import show_menu_ab

router = Router(name="chat")



@router.message(F.text == kb_maine_ad)
async def menu_ad(m: Message):
    await show_menu_ab(m)

@router.message(F.text == kb_maine_help)
async def help_kb(m: Message):
    await m.answer(help_text, parse_mode="HTML")

@router.message(F.text == kb_maine_hide)
async def hide_kb(m: Message):
    await m.answer(reply_markup=ReplyKeyboardRemove())

