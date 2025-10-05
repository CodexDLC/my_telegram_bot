# app/handlers/callback/random_handler.py
import logging

from aiogram import F, Router
from aiogram.types import CallbackQuery, Message

from app.resources.keyboards.inline import random_inline_kb
from app.services.llm_provider import get_llm_answer

log = logging.getLogger(__name__)

router = Router(name="random_fact")
order_text = "Расскажи рандомный факт"


@router.callback_query(F.data == "fact_random")
async def fact_random_handler(call: CallbackQuery)-> None:
    user_id = call.from_user.id if call.from_user else None
    answer_fn = get_llm_answer(user_id)

    response = await answer_fn("random_fact", order_text)
    if isinstance(call.message, Message):
        await call.message.edit_text(response, reply_markup=random_inline_kb())
