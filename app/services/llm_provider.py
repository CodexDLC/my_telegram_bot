from __future__ import annotations
import os
import logging
from typing import Callable, Any, Dict, Optional

from app.services.gemini_service.gemini_service import gemini_answer
from app.services.gpt_service.chat_gpt_service import gpt_answer as gpt_answer_openai

log = logging.getLogger(__name__)

# Тип для возвращаемой функции (сам сервис, gpt_answer или gemini_answer)
LLMFunction = Callable[..., Any]

# Словарь наших сервисов
LLM_SERVICES: Dict[str, LLMFunction] = {
    "openai": gpt_answer_openai,
    "gemini": gemini_answer,
}

# Получаем модель по умолчанию из .env
DEFAULT_MODEL_NAME = os.getenv("DEFAULT_LLM", "openai")
# Получаем сервис по умолчанию на случай, если в LLM_SERVICES нет DEFAULT_MODEL_NAME
DEFAULT_SERVICE = LLM_SERVICES.get(DEFAULT_MODEL_NAME, gemini_answer)


def get_llm_answer(user_row: Optional[Dict[str, Any]]) -> LLMFunction:
    """
    Получает 'строку' пользователя из БД (или None)
    и возвращает нужную LLM-функцию (gpt_answer или gemini_answer).

    Этот сервис больше НЕ ходит в базу данных.
    """
    model_name = DEFAULT_MODEL_NAME

    if user_row:
        # Пытаемся взять модель из строки БД
        # .get() вернет None, если ключа 'llm_model' нет
        model_name = user_row["llm_model"] or model_name

    log.debug(f"Выбрана модель '{model_name}' для пользователя.")

    # Возвращаем ФУНКЦИЮ
    # Если .get() не найдет model_name, он вернет сервис по умолчанию
    return LLM_SERVICES.get(model_name, DEFAULT_SERVICE)
