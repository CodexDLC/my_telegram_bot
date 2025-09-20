# presentation/route/commands.py
import logging

from app.resources.text import help_text

log = logging.getLogger(__name__)

from app.resources.keyboards.keyboard import main_kb
from app.resources.text import start_text

from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.filters import Command

router = Router(name="commands_router")


@router.message(Command("start"))
async def start_handler(m: Message, state: FSMContext):
    log.info("Команда /start")
    await state.clear()
    await m.answer(start_text, parse_mode="HTML", reply_markup=main_kb(), )


@router.message(Command("help"))
async def help_handler(m: Message):
    log.info("Команда /help")
    await m.answer(help_text, parse_mode="HTML")

