# app/handlers/setting_callback/model_selection.py
import logging

from aiogram import F, Router
from aiogram.types import CallbackQuery

from app.resources.keyboards.inline import setting_model_selection_inline_kb
from database.db import get_db_connection
from database.repositories import get_user_repo

log = logging.getLogger(__name__)

router = Router(name="model_selection")


@router.callback_query(F.data == "model_selection")
async def model_selection_handler(call: CallbackQuery) -> None:
    """
    Показывает клавиатуру выбора модели.
    Теперь он сначала лезет в БД, чтобы узнать текущую
    модель пользователя и правильно отобразить '✅'.
    """
    user_id = call.from_user.id if call.from_user else None
    current_model = None

    if user_id:
        try:
            async with get_db_connection() as db:
                user_repo = get_user_repo(db)
                user_row = await user_repo.get_user(user_id)
                if user_row:
                    current_model = user_row["llm_model"]
            log.info(f"Текущая модель для {user_id}: {current_model}")
        except Exception as e:
            log.error(f"Ошибка получения модели для {user_id}: {e}")

    # Передаем текущую модель в клавиатуру
    await call.message.edit_text(
        "Выберите модель",
        reply_markup=setting_model_selection_inline_kb(current_model)
    )


@router.callback_query(F.data.startswith("model:"))
async def apply_model_handler(call: CallbackQuery) -> None:
    """
    Обрабатывает нажатие на кнопку модели и ОБНОВЛЯЕТ
    выбор пользователя в базе данных.
    """
    data = call.data
    model = ""
    if data is not None:
        model = data.split(":")[-1]
        log.info(f"Выбранная модель: {model}")

    user_id = call.from_user.id if call.from_user else None

    if not user_id:
        await call.answer("Не могу определить ID пользователя!", show_alert=True)
        return

    try:
        # 1. Хэндлер открывает коннект
        async with get_db_connection() as db:
            # 2. Хэндлер получает репозиторий
            user_repo = get_user_repo(db)
            # 3. Хэндлер выполняет логику (запись в БД)
            await user_repo.update_user_model(user_id=user_id, model_name=model)

        log.info(f"Модель для {user_id} обновлена на {model}")

        # Обновляем сообщение, передавая новую модель для '✅'
        await call.message.edit_text(
            f"Модель выбрана: {model}",
            reply_markup=setting_model_selection_inline_kb(model)
        )
    except Exception as e:
        log.error(f"Ошибка обновления модели для {user_id}: {e}")
        await call.answer("Произошла ошибка при сохранении выбора.", show_alert=True)
