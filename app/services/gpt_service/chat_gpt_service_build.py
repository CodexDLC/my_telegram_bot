from typing import Any, Callable, List

from openai.types.chat import (
    ChatCompletionDeveloperMessageParam,
    ChatCompletionMessageParam,
    ChatCompletionSystemMessageParam,
    ChatCompletionUserMessageParam,
)

from app.resources.assets.dict_preset import ChatMode, ModePreset
from app.resources.assets.quiz_theme import DEV_SQUIZ
from app.resources.assets.recommen_dict import resp_reco


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
    user_text: str | Any,
    **kw: Any
) -> List[ChatCompletionMessageParam]:

    topic = kw["topic"]
    difficulty = kw["difficulty"]
    context = kw.get("context")

    dev: ChatCompletionDeveloperMessageParam = {
        "role": "developer",
        "content": f"{preset['developer']} : Выдавай ОДИН вопрос Quiz по теме {topic} и сложности {difficulty}. "
                   f"КАТЕГОРИЧЕСКИ ЗАПРЕЩЕНО повторять вопросы из этого списка: [{context}]. "
                   f"{DEV_SQUIZ}"

    }
    sys: ChatCompletionSystemMessageParam = {
        "role": "system",
        "content": preset["system"],
    }
    usr: ChatCompletionUserMessageParam = {"role": "user", "content": user_text}

    return [dev, sys, usr]




def build_chat(
    preset: ModePreset,
    user_text: str,
    **kw: Any
) -> List[ChatCompletionMessageParam] | Any:


    his = kw.setdefault("history", [])

    dev: ChatCompletionDeveloperMessageParam = {
        "role": "developer",
        "content": preset["developer"],
    }
    sys: ChatCompletionSystemMessageParam = {
        "role": "system",
        "content": preset["system"],
    }

    return [dev, sys] + his



def build_recommendation(
    preset: ModePreset,
    user_text: str,
    **kw: Any
) -> List[ChatCompletionMessageParam]:

    apply_label = kw.get("apply_label")
    str_label = ", ".join(apply_label)
    old = kw.get("exceptions") or []
    exceptions = ", ".join(old)
    category = kw.get("category") or ""


    dev: ChatCompletionDeveloperMessageParam = {
        "role": "developer",
        "content": f"{preset["developer"]}"
                   f"Учитывай категорию {category} и жанры для нее:{str_label} под настроение и похожесть жанров. "
                   f"исключай старые рекомендации {exceptions}. "
                   f"{resp_reco}"
    }
    sys: ChatCompletionSystemMessageParam = {
        "role": "system",
        "content": preset["system"],
    }

    return [dev, sys]





Builder = Callable[..., list[ChatCompletionMessageParam]]

BUILDERS_GPT: dict[ChatMode, Builder] = {
    "random_fact": build_default,
    "chat": build_chat,
    "persona": build_persona,
    "quiz": build_quiz,
    "translate": build_default,
    "reco": build_recommendation,
}
