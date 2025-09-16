from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message

from presentation.keyboards.keyboard import confirm_kb

router = Router(name="adv_create")

class AdCreate(StatesGroup):
    WAIT_CONTENT = State()
    CONFIRM      = State()


@router.message(StateFilter(AdCreate.WAIT_CONTENT), F.text & ~F.via_bot)
async def wait_text(m: Message, state: FSMContext):
    text = (m.text or " ").strip()
    if not text:
        await m.answer("Нельзя отправлять пустой текст")
        return

    # Записываем сообщение в память
    await state.update_data(kind="text", text=text, file_id=None)

    # Отправляем сообщение пользователю
    await m.answer(f"Принял текст объявления:\n\n{text}")


@router.message(StateFilter(AdCreate.WAIT_CONTENT), F.foto)
async def wait_foto(m: Message, state: FSMContext):
    largest = m.photo[-1]
    file_id = largest.file_id
    caption = (m.caption or "").strip()

    await state.update_data(kind="foto", text=caption, file_id=file_id)
    await m.answer_photo(photo=file_id, caption=caption or "Фото без подписи")


@router.message(StateFilter(AdCreate.WAIT_CONTENT), F.voice)
async def wait_voice(m: Message, state: FSMContext):
    file_id = m.voice.file_id
    caption = (m.caption or "").strip()

    await state.update_data(kind="audio",  caption=caption, file_id=file_id)

