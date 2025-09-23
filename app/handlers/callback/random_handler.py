# app/handlers/callback/random_handler.py
import logging

from app.resources.keyboards.inline import random_inline_kb

log = logging.getLogger(__name__)

from aiogram.types import Message, CallbackQuery

from app.services.chat_gpt_service import gpt_answer



from aiogram import Router, F


router = Router(name="random_fact")
order_text = "Расскажи рандомный факт"


@router.callback_query(F.data == "fact_random")
async def fact_random_handler(call: CallbackQuery):
    response = await gpt_answer("random_fact", order_text)
    await call.message.edit_text(response, reply_markup=random_inline_kb())


