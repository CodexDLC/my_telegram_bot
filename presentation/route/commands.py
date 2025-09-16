
from typing import Any

from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from presentation.keyboards.keyboard import start_keyboard
from presentation.text.start import start_text

command_router = Router(name="commands_router")


@command_router.message(Command("start"))
async def start_handler(message: Message) -> Any:
    keyword = start_keyboard()
    await message.answer(start_text, parse_mode="HTML")
    await message.answer(keyword)

@command_router.message(Command("help"))
async def help_handler(message: Message):
    await message.answer("Тут будет помощь")


@command_router.message(Command("announcement"))
async def announcement_handler(message: Message):
    await message.answer("Обработка логики создания обьявления")


@command_router.message(Command("list"))
async def list_announcement_handler(message: Message):
    await message.answer("Обработка логики показать все сохраненные обьявления ")








