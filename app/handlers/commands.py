# presentation/route/commands.py
import logging
log = logging.getLogger(__name__)

from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.filters import Command

from app.resources.text.anonce import start_text
from app.resources.keyboards.reply import main_kb

router = Router(name="commands_router")


@router.message(Command("start"))
async def start_handler(m: Message, state: FSMContext):
    log.info("Команда /start")
    await m.answer("Старт меню", reply_markup=main_kb())



