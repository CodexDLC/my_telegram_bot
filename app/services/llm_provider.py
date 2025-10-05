# app/services/llm_provider.py

import os
import google.generativeai as genai

# Импортируем обе функции
from app.services.gpt_service.chat_gpt_service import gpt_answer as gpt_answer_openai
# from app.services.gemini_service import gemini_answer as gpt_answer_gemini # Пока условно

# Хранилище для активной функции
_active_llm_answer = None

# Словарь для выбора функции по названию
LLM_SERVICES = {
    "openai": gpt_answer_openai,
    # "gemini": gpt_answer_gemini,
}


def set_active_llm(model_name: str) -> bool:
    """Устанавливает активную языковую модель."""
    global _active_llm_answer
    if model_name in LLM_SERVICES:
        _active_llm_answer = LLM_SERVICES[model_name]
        return True
    return False

def get_llm_answer():
    """Возвращает функцию для ответа текущей активной модели."""
    global _active_llm_answer
    if _active_llm_answer is None:
        # Устанавливаем модель по умолчанию при первом запуске
        default_model = os.getenv("DEFAULT_LLM", "openai")
        set_active_llm(default_model)
    return _active_llm_answer