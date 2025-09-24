from typing import List, Callable, Any

from openai.types.chat import (
    ChatCompletionDeveloperMessageParam,
    ChatCompletionMessageParam,
    ChatCompletionSystemMessageParam,
    ChatCompletionUserMessageParam,
)

from app.resources.assets.dict_preset import ModePreset, ChatMode
from app.resources.assets.quiz_theme import DEV_SQUIZ


def build_default(
    preset: ModePreset,
    user_text: str,
    **kw: Any
) -> List[ChatCompletionMessageParam]:

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


def build_persona(
    preset: ModePreset,
    user_text: str,
    **kw: Any
) -> List[ChatCompletionMessageParam]:

    role_hint = kw["role_hint"]

    dev: ChatCompletionDeveloperMessageParam = {
        "role": "developer",
        "content": f"{preset['developer']} Роль: {role_hint}".strip(),
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


def build_quiz(
    preset: ModePreset,
    user_text: str,
    **kw: Any
) -> List[ChatCompletionMessageParam]:

    topic = kw["topic"]
    difficulty = kw["difficulty"]

    dev: ChatCompletionDeveloperMessageParam = {
        "role": "developer",
        "content": f"{preset['developer']} : Выдавай ОДИН вопрос Quiz по теме {topic} и сложности {difficulty} "                   
                   f"{DEV_SQUIZ}"
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
    "persona": build_persona,
    "quiz": build_quiz,
    "translate": build_default,
    "reco": build_default,
}
