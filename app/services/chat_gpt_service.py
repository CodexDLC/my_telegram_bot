import logging
from typing import List, Callable, Dict, Any

from openai.types.chat import ChatCompletionDeveloperMessageParam, ChatCompletionMessageParam, \
    ChatCompletionSystemMessageParam, ChatCompletionUserMessageParam

log = logging.getLogger(__name__)

from app.resources.assets.dict_preset import ChatMode, MODE_PRESETS, ModePreset

from openai import AsyncOpenAI

from app.core.config import GPT_TOKEN

GPT_MODEL_DEFAULT = "gpt-4o-mini"
client = AsyncOpenAI(api_key=GPT_TOKEN)


def build_default(preset: ModePreset, user_text: str, **kw) -> List[ChatCompletionMessageParam]:

    dev: ChatCompletionDeveloperMessageParam = {
        "role": "developer",
        "content": preset["developer"],
    }
    sys: ChatCompletionSystemMessageParam = {
        "role": "system",
        "content": preset["system"],
    }
    usr: ChatCompletionUserMessageParam = {
        "role": "user",
        "content": user_text,
    }
    return [dev, sys, usr]


def build_persona(preset: ModePreset, user_text: str, **kw) -> List[ChatCompletionMessageParam]:
    role_hint = kw['role_hint']

    dev: ChatCompletionDeveloperMessageParam = {
        "role": "developer",
        "content": f"{preset['developer']} Роль: {role_hint}".strip()
    }
    sys: ChatCompletionSystemMessageParam = {
        "role": "system",
        "content": preset["system"],
    }
    usr: ChatCompletionUserMessageParam = {
        "role": "user",
        "content": user_text,
    }
    return [dev, sys, usr]




Builder = Callable[..., list[ChatCompletionMessageParam]]
BUILDERS: dict[ChatMode, Builder] = {
    "random_fact": build_default,
    "chat": build_default,
    "persona" : build_persona,
    "quiz": None,
    "translate" : build_default,
    "reco" : build_default,

}


async def gpt_answer(mode: ChatMode, user_text: str, **kw: Any) -> str:
    preset = MODE_PRESETS[mode]
    log.info(f"preset")
    bild_msg = BUILDERS.get(mode, build_default)

    msg = bild_msg(preset, user_text, **kw)

    log.debug(f"В сообщение вот такое состав {msg}")

    temperature = kw.get("temperature", preset["temperature"])
    max_tokens  = kw.get("max_tokens",  preset["max_tokens"])

    resp = await client.chat.completions.create(
        model=GPT_MODEL_DEFAULT,
        messages=msg,
        temperature=temperature,
        max_tokens=max_tokens
    )
    return resp.choices[0].message.content or ""

