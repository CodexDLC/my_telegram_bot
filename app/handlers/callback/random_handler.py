# app/handlers/callback/random_handler.py
import logging

from aiogram import F, Router
from aiogram.types import CallbackQuery, Message

from app.resources.keyboards.inline import random_inline_kb
from app.services.llm_provider import get_llm_answer
from database.db import get_db_connection
from database.repositories import get_user_repo

log = logging.getLogger(__name__)

router = Router(name="random_fact")
order_text = "Расскажи рандомный факт"


@router.callback_query(F.data == "fact_random")
async def fact_random_handler(call: CallbackQuery)-> None:
    user_id = call.from_user.id if call.from_user else None

    async with get_db_connection() as db:
        user_repo = get_user_repo(db)
        user_row = await user_repo.get_user(user_id)

    answer_fn = get_llm_answer(user_row)
    log.info(answer_fn)
    response = await answer_fn("random_fact", order_text)
    if isinstance(call.message, Message):
        await call.message.edit_text(response, reply_markup=random_inline_kb())
