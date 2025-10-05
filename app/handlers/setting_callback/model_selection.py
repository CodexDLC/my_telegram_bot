# app/handlers/setting_callback/model_selection.py
import logging

from aiogram import F, Router
from aiogram.types import CallbackQuery

from app.resources.keyboards.inline import setting_model_selection_inline_kb
from app.services.llm_provider import set_active_llm

log = logging.getLogger(__name__)

router = Router(name="model_selection")


@router.callback_query(F.data == "model_selection")
async def model_selection_handler(call: CallbackQuery)-> None:
    await call.message.edit_text("Выберите модель", reply_markup=setting_model_selection_inline_kb())




@router.callback_query(F.data.startswith("model:"))
async def apply_model_handler(call: CallbackQuery)-> None:
    data = call.data
    if data is not None:
        model = data.split(":")[-1]
        log.info(f"Выбранная модель: {model}")
    else:
        model = ""
    user_id = call.from_user.id if call.from_user else None

    set_active_llm(model_name=model, user_id=user_id)

    await call.message.edit_text(f"Модель выбрана: {model}",reply_markup=setting_model_selection_inline_kb(model))
