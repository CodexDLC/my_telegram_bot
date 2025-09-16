from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from constant.callback import CONFIRM_SAVE
from infrastructure.repositor.adv_repo import AdvRepo
from presentation.keyboards.keyboard import confirm_kb
from presentation.route.FSM.add_fsm import AdCreate


router = Router(name="confirm")


async def goto_confirm(message: Message, state: FSMContext) -> None:
    data   = await state.get_data()            # {kind, text, file_id, tags?}
    kind   = data.get("kind")
    text   = (data.get("text") or "").strip()
    file_id= data.get("file_id")
    kb     = confirm_kb()

    await state.set_state(AdCreate.CONFIRM)

    # Превью по типу контента
    if kind == "text":
        await message.answer(f"Предпросмотр объявления:\n\n{text}", reply_markup=kb)
    elif kind == "photo" and file_id:
        await message.answer_photo(photo=file_id, caption=text or "Без подписи", reply_markup=kb)
    elif kind == "voice" and file_id:
        await message.answer_voice(voice=file_id, caption=text or "Без подписи", reply_markup=kb)
    else:
        await message.answer("Не понимаю черновик. Пришлите текст/фото/voice заново.")
        await state.set_state(AdCreate.WAIT_CONTENT)


@router.callback_query(StateFilter(AdCreate.CONFIRM), F.data == CONFIRM_SAVE)
async def on_confirm_save(call: CallbackQuery, state: FSMContext, ):
    await call.answer()
    draft = await state.get_data()
    repo = AdvRepo()

    # TODO: здесь твоё сохранение (БД/файл/память). Ниже — заглушка id.
    await repo.save_adv_data(draft)

    await state.clear()



