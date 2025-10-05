# app/services/chat_gpt_service.py
import logging
from typing import Any

from openai import AsyncOpenAI

from app.core.config import GPT_TOKEN
from app.resources.assets.dict_preset import MODE_PRESETS, ChatMode
from app.services.gpt_service.chat_gpt_service_build import BUILDERS, build_default

log = logging.getLogger(__name__)

GPT_MODEL_DEFAULT = "gpt-4o-mini"
client = AsyncOpenAI(api_key=GPT_TOKEN)


async def gpt_answer(mode: ChatMode, user_text: str, **kw: Any) -> str:

    preset = MODE_PRESETS[mode]
    log.info(f"Выбран preset: {mode}")
    builder_func = BUILDERS.get(mode)

    # Если функция не найдена (результат None), используем конструктор по умолчанию.
    if builder_func is None:
        builder_func = build_default

    msg = builder_func(preset, user_text, **kw)

    log.debug(f"В сообщение вот такое состав {msg}")

    temperature = kw.get("temperature", preset["temperature"])
    max_tokens = kw.get("max_tokens", preset["max_tokens"])

    resp = await client.chat.completions.create(
        model=GPT_MODEL_DEFAULT,
        messages=msg,
        temperature=temperature,
        max_tokens=max_tokens,
        presence_penalty=0.6,

    )
    return resp.choices[0].message.content or ""
