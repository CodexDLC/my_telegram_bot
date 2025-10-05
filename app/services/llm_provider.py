# app/services/llm_provider.py
from __future__ import annotations
import os
from typing import Dict

from app.services.gemini_service.gemini_service import gemini_answer
from app.services.gpt_service.chat_gpt_service import gpt_answer as gpt_answer_openai

# как и было
_active_llm_answer = None

LLM_SERVICES = {
    "openai": gpt_answer_openai,
    "gemini": gemini_answer,
}

# новое: карта "пользователь -> выбранный провайдер"
_user_llm_provider: Dict[int, str] = {}


def set_active_llm(model_name: str, user_id: int | None = None) -> bool:
    """
    Если user_id=None — ставим ГЛОБАЛЬНО.
    Если user_id указан — сохраняем выбор только для этого пользователя.
    """
    if model_name not in LLM_SERVICES:
        return False

    if user_id is None:
        global _active_llm_answer
        _active_llm_answer = LLM_SERVICES[model_name]
    else:
        _user_llm_provider[user_id] = model_name
    return True


def get_llm_answer(user_id: int | None = None):
    """
    Если есть индивидуальный выбор для user_id — вернём его.
    Иначе используем глобальный активный (или дефолт из ENV).
    """
    if user_id is not None:
        model_name = _user_llm_provider.get(user_id)
        if model_name:
            return LLM_SERVICES[model_name]

    global _active_llm_answer
    if _active_llm_answer is None:
        default_model = os.getenv("DEFAULT_LLM", "openai")
        set_active_llm(default_model)
    return _active_llm_answer