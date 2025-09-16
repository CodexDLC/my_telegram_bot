# presentation/route/commands.py

from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from presentation.keyboards.keyboard import start_inline_kb
from presentation.text.start import start_text

router = Router(name="commands_router")

@router.message(Command("start"))
async def start_handler(message: Message):
    kb = start_inline_kb()
    await message.answer(start_text, parse_mode="HTML", reply_markup=kb)

@router.message(Command("help"))
async def help_handler(m: Message):
    await m.answer("Тут будет помощь")





