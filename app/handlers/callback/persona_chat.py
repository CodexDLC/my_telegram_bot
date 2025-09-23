import logging

from app.resources.assets.dict_preset import ROLE_SPECS
from app.resources.assets.states import PersonTalk
from app.resources.keyboards.inline import chat_inline_kb, get_person_inline_kb, person_inline_kb
from app.resources.text.anonce import start_text
from app.services.chat_gpt_service import gpt_answer

log = logging.getLogger(__name__)

from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.types import Message


router  = Router(name="persona_chat")

MAX_LEN = 2048

@router.callback_query(F.data == "dialog_persona")
async def persona_start_handler(call: CallbackQuery, state: FSMContext):
    """
    :param call: Начало диалога
    :param state: вызывает состояние TEXT_TRANSLATE
    :return: возращает сообщение выбрать личность и клавиатуру со списком личностей
    """
    await call.answer()
    await state.set_state(PersonTalk.TEXT_PERSONA)
    await call.message.edit_text("Выбери личность", parse_mode="HTML", reply_markup=get_person_inline_kb())

@router.callback_query(F.data.startswith("ROLE:"))
async def set_persona_handler(call: CallbackQuery, state: FSMContext):
    """
    :param call: ловим сигнал о личности
    :param state: TEXT_TRANSLATE state не меняется
    :return: редактируем последите сообщения сообщаем о выбранной роли ждем сообщений для общения
                возвращаем клавиатуру со сменой личности и возвратом в главное меню
    """
    await state.set_state(PersonTalk.TEXT_PERSONA)
    role_new = call.data.split(":", 1)[1]
    role_present = ROLE_SPECS[role_new]['label']
    await state.update_data(role=role_new)
    new_role_text = f"Роль изменена на {role_present}"
    await call.message.edit_text(new_role_text, reply_markup=person_inline_kb())


@router.message(StateFilter(PersonTalk.TEXT_PERSONA), F.text)
async def fsm_text_persona_handler(m: Message, state: FSMContext):
    """
    :param m: Обработка текстовых сообщений и общения с личностью. Проверяет что бы был текст и не очень длинный
    :param state: TEXT_TRANSLATE
    :return: возвращает отредактированное сообщение бота которое он отправляет пока думает
    """
    if not m.text:
        await m.answer("Нужен обычный текст.")
    elif len(m.text) > MAX_LEN:
        await m.answer(f"Нужен текст до {MAX_LEN} символов вы отправили {len(m.text)} символов.")
        return

    data = await state.get_data()
    role = data.get("role", "einstein")
    spec = ROLE_SPECS[role]
    role_hint = spec["hint"]
    log.info(f"{role_hint}")
    chat_text = m.text
    msg_role = await m.answer(f"{spec['label']} думает")
    response = await gpt_answer("persona", chat_text, role_hint=role_hint, temperature=spec["temperature"], max_tokens=spec["max_tokens"])
    await msg_role.edit_text(response, reply_markup=chat_inline_kb())


# Так дальше обработка клавиатуры возврата в главное меню или смены личности

@router.callback_query(F.data == "switch_role")
async def switch_persona_handler(call: CallbackQuery, state: FSMContext):
    log.info("Поймали сообщение о смене роли")
    await state.set_state(PersonTalk.TEXT_PERSONA)
    await call.message.edit_text("Выбери личность", parse_mode="HTML", reply_markup=get_person_inline_kb())


@router.callback_query(F.data == "🔙 Вернуться в меню")
async def cancel_persona_handler(call: CallbackQuery, state: FSMContext, msg=None):
    log.debug("Поймали сообщение: '🔙 Вернуться в меню'")
    await msg.edit_text(start_text, parse_mode="HTML", reply_markup=chat_inline_kb())
    await state.clear()
