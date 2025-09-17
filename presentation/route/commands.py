# presentation/route/commands.py

from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.filters import Command

from services.handlers_command.start_menu import show_start_menu

router = Router(name="commands_router")

@router.message(Command("start"))
async def start_handler(m: Message, state: FSMContext):
    await state.clear()
    await show_start_menu(m)

@router.message(Command("help"))
async def help_handler(m: Message):
    await m.answer("Тут будет помощь")





