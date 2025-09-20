# presentation/route/callback/start_menu.py

from aiogram import Router, F
from aiogram.fsm.context import FSMContext

from aiogram.types import CallbackQuery
from app.constant.callback import ADV_CREATE, ADV_LIST, ADV_FIND
from app.handlers.FSM.add_fsm import AdCreate

router = Router(name="adv_start_menu")
# Ловим только свои payload
router.callback_query.filter(F.data.startswith("adv:"))


@router.callback_query(F.data == ADV_CREATE)
async def cb_create(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await state.set_state(AdCreate.WAIT_CONTENT)
    await call.message.edit_text(
        "Пришлите текст объявления одним сообщением.", reply_markup=None
    )


@router.callback_query(F.data == ADV_LIST)
async def cb_list(call: CallbackQuery):
    await call.answer()
    await call.message.edit_text("Здесь будет список ваших объявлений.")
    # TODO: Добавить логику вывода списка задач из базы.


@router.callback_query(F.data == ADV_FIND)
async def cb_find(call: CallbackQuery):
    await call.answer()
    await call.message.edit_text("Здесь будет поиск.")
    # TODO: Добавить ожидание ключа и вывод объявлений по ключу
