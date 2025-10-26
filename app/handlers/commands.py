# app/handlers/commands.py
import logging

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from app.resources.keyboards.reply import main_kb
from database.db import get_db_connection
from database.repositories import get_user_repo

log = logging.getLogger(__name__)

router = Router(name="commands_router")


@router.message(Command("start"))
async def start_handler(m: Message)-> None:
    log.info("Команда /start")
    async with get_db_connection() as db:
        user_repo = get_user_repo(db)
        await user_repo.upsert_user(
            user_id=m.from_user.id,
            first_name=m.from_user.first_name,
            username=m.from_user.username)
    await m.answer("Старт меню", reply_markup=main_kb())
