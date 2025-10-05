
from typing import Callable, Any, List, Tuple, Dict

from google.genai import types
from app.resources.assets.dict_preset import ModePreset, ChatMode
from app.resources.assets.quiz_theme import DEV_SQUIZ
from app.resources.assets.recommen_dict import resp_reco


def _sys(preset: ModePreset, extra: str | None = None) -> str:
    dev = (preset.get("developer") or "").strip()
    sys = (preset.get("system") or "").strip()
    add = (extra or "").strip()
    parts = [p for p in (dev, sys, add) if p]
    return "\n\n".join(parts)

def history_to_gemini_contents_raw(
    history: List[Dict[str, str]],
    keep: int = 5,
) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    for m in history[-keep:]:
        role = "user" if m["role"] == "user" else "model"
        out.append({"role": role, "parts": [{"text": m["content"]}]})
    return out


def build_default_gemini(
    preset: ModePreset, user_text: str, **kw: Any
) -> tuple[str, str]:
    contents = user_text
    return contents, _sys(preset)


def build_persona_gemini(
    preset: ModePreset, user_text: str, **kw: Any
) -> tuple[str, str]:
    role_hint = kw["role_hint"]
    extra = f"Роль: {role_hint}"
    contents = user_text
    return contents, _sys(preset, extra)

def build_chat_gemini(
    preset: ModePreset, user_text: str, **kw: Any
) -> tuple[list[dict[str, Any]], str]:
    his = kw.setdefault("history", [])
    keep = len(his)
    contents = history_to_gemini_contents_raw(his, keep)
    if not contents:
        contents = [{"role": "user", "parts": [{"text": user_text}]}]

    return contents, _sys(preset)

def build_quiz_gemini(
    preset: ModePreset, user_text: str | Any, **kw: Any
) -> Tuple[List[types.Content], str]:
    topic = kw["topic"]
    difficulty = kw["difficulty"]
    context = kw.get("context")

    if isinstance(context, (list, tuple)):
        context_str = ", ".join(map(str, context))
    else:
        context_str = str(context) if context is not None else ""

    extra = (
        f"Выдавай ОДИН вопрос Quiz по теме {topic} и сложности {difficulty}. "
        f"КАТЕГОРИЧЕСКИ ЗАПРЕЩЕНО повторять вопросы из этого списка: [{context_str}]. "
        f"{DEV_SQUIZ}"
    )

    contents = user_text or ""
    return contents, _sys(preset, extra)

def build_recommendation_gemini(
    preset: ModePreset, user_text: str, **kw: Any
) -> tuple[str, str]:
    apply_label = kw.get("apply_label") or []
    str_label = ", ".join(apply_label)

    old = kw.get("exceptions") or []
    exceptions = ", ".join(old)

    category = kw.get("category") or ""

    extra = (
        f"Учитывай категорию {category} и жанры для неё: {str_label} "
        f"под настроение и похожесть жанров. "
        f"Исключай старые рекомендации: {exceptions}. "
        f"{resp_reco}"
    )

    contents = user_text or ""
    return contents, _sys(preset, extra)



GeminiBuilder = Callable[..., Tuple[List[types.Content], str]]

BUILDERS_GEMENI: dict[ChatMode, GeminiBuilder] = {
    "random_fact": build_default_gemini,
    "chat": build_chat_gemini,
    "persona": build_persona_gemini,
    "quiz": build_quiz_gemini,
    "translate": build_default_gemini,
    "reco": build_recommendation_gemini,
}