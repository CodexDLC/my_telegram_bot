# app/handlers/commands.py
import logging

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from app.resources.keyboards.reply import main_kb

log = logging.getLogger(__name__)

router = Router(name="commands_router")


@router.message(Command("start"))
async def start_handler(m: Message)-> None:
    log.info("Команда /start")
    await m.answer("Старт меню", reply_markup=main_kb())
