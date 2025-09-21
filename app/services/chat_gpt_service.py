import logging
from typing import List

from openai.types.chat import ChatCompletionDeveloperMessageParam, ChatCompletionMessageParam, \
    ChatCompletionSystemMessageParam, ChatCompletionUserMessageParam

log = logging.getLogger(__name__)

from app.resources.assets.dict_preset import ChatMode, MODE_PRESETS, ModePreset

from openai import AsyncOpenAI

from app.core.config import GPT_TOKEN

GPT_MODEL_DEFAULT = "gpt-4o-mini"
client = AsyncOpenAI(api_key=GPT_TOKEN)


def _create_message(preset: ModePreset, user_text: str) -> List[ChatCompletionMessageParam]:
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


async def gpt_answer(mode: ChatMode, user_text: str,*args,) -> str:
    preset = MODE_PRESETS[mode]
    log.info(f"preset")

    msg = _create_message(preset, user_text)
    log.info("msg")

    resp = await client.chat.completions.create(
        model=GPT_MODEL_DEFAULT,
        messages=msg,
        temperature=preset["temperature"],
        max_tokens=preset["max_tokens"]
    )
    return resp.choices[0].message.content or ""

