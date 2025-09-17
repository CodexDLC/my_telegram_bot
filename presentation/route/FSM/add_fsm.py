from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery

from constant.callback import CONFIRM_SAVE, CONFIRM_CANCEL, CONFIRM_BACK
from constant.kind import kind_text, kind_photo, kind_voice
from infrastructure.repositor.adv_repo import FileAdvRepo
from presentation.keyboards.keyboard import confirm_kb
from services.handlers_command.start_menu import show_start_menu

router = Router(name="adv_create")


class AdCreate(StatesGroup):
    WAIT_CONTENT = State()
    CONFIRM = State()


@router.message(StateFilter(AdCreate.WAIT_CONTENT), F.text & ~F.via_bot)
async def wait_text(m: Message, state: FSMContext):
    user_id = m.from_user.id
    text = (m.text or " ").strip()
    if not text:
        await m.answer("Нельзя отправлять пустой текст")
        return
    # Записываем сообщение в память
    await state.update_data(user_id = user_id, kind=kind_text, text=text, file_id=None, )
    await goto_confirm(message=m, state=state)


@router.message(StateFilter(AdCreate.WAIT_CONTENT), F.photo)
async def wait_photo(m: Message, state: FSMContext):
    user_id = m.from_user.id
    largest = m.photo[-1]
    file_id = largest.file_id
    caption = (m.caption or "").strip()
    # Записываем фото и подпись в память
    await state.update_data(user_id = user_id, kind=kind_photo, text=caption, file_id=file_id)
    await goto_confirm(message=m, state=state)


@router.message(StateFilter(AdCreate.WAIT_CONTENT), F.voice)
async def wait_voice(m: Message, state: FSMContext):
    user_id = m.from_user.id
    file_id = m.voice.file_id
    # Записываем голосовое в память сообщение в память
    await state.update_data(user_id = user_id, kind=kind_voice, file_id=file_id)
    await goto_confirm(message=m, state=state)


@router.message(StateFilter(AdCreate.WAIT_CONTENT))
async def wait_unsupported(m: Message):
    await m.answer(
        "Мне нужен текст, фото или голосовое. Попробуй ещё раз. /cancel — отмена."
    )


async def goto_confirm(message: Message, state: FSMContext) -> None:

    data = await state.get_data()
    kind = data.get("kind")
    text = (data.get("text") or "").strip()
    file_id = data.get("file_id")
    kb = confirm_kb()

    await state.set_state(AdCreate.CONFIRM)

    # Превью по типу контента
    if kind == kind_text:
        await message.answer(f"Предпросмотр объявления:\n\n{text}", reply_markup=kb)
    elif kind == kind_photo and file_id:
        await message.answer_photo(
            photo=file_id, caption=text or "Без подписи", reply_markup=kb
        )
    elif kind == kind_voice and file_id:
        await message.answer_voice(voice=file_id, reply_markup=kb)
    else:
        await message.answer("Не понимаю черновик. Пришлите текст/фото/voice заново.")
        await state.set_state(AdCreate.WAIT_CONTENT)


@router.callback_query(StateFilter(AdCreate.CONFIRM), F.data == CONFIRM_SAVE)
async def on_confirm_save(
    call: CallbackQuery,
    state: FSMContext,
):
    draft = await state.get_data()
    repo = FileAdvRepo(draft)

    await repo.save_adv_data()
    await state.clear()
    await show_start_menu(call)


@router.callback_query(StateFilter(AdCreate.CONFIRM), F.data == CONFIRM_BACK)
async def adv_back(
    call: CallbackQuery,
    state: FSMContext,
):
    await state.set_state(AdCreate.WAIT_CONTENT)
    await call.message.edit_text("Введите ваше объявление заново", reply_markup=None)


@router.callback_query(StateFilter(AdCreate.CONFIRM), F.data == CONFIRM_CANCEL)
async def adv_cancel(call: CallbackQuery, state: FSMContext):
    await state.clear()
    await show_start_menu(call)
