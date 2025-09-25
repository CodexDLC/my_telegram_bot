# app/services/context_service.py
import logging


log = logging.getLogger(__name__)

chat_histories: dict[int, dict[str, list]] = {}
MAX_HISTORY_LENGTH = 15

async def add_message(user_id: int, mode: str, role: str, text: str):

    # Получаем историю или создаем новую
    user_history = chat_histories.setdefault(user_id, {})

    # Получаем историю режима
    history_list = user_history.setdefault(mode, [])
    log.debug(f"История режима {history_list}")

    # Собираем данные для сохранения
    new_message = {"role": role, "content": text}
    log.debug(f"История для сохранения {new_message}")

    # Обновляем историю режима
    history_list.append(new_message)

    # Если буфер переполнен чистим на 1 сообщение
    if len(history_list) > MAX_HISTORY_LENGTH:
        history_list.pop(0)

    log.info(f"История для {user_id} обновлена. Длина: {len(history_list)}")

async def get_history(user_id: int, mode: str) -> list:

    user_history = chat_histories.get(user_id, {})

    history_list = user_history.get(mode, [])

    log.info(f"Данные пользователя {user_id} по истории чата мода {mode} выданы")
    log.debug(f"История чата {history_list}")
    return history_list