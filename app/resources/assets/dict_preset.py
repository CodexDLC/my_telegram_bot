# app/resources/assets/dict_preset.py
from __future__ import annotations

from typing import Dict, Literal, TypedDict

ChatMode = Literal["random_fact", "chat", "persona", "quiz", "translate", "reco"]


class ModePreset(TypedDict):
    developer: str
    system: str
    temperature: float
    max_tokens: int


MODE_PRESETS: Dict[ChatMode, ModePreset] = {
    "random_fact": {
        "developer": "Отвечай одним любопытным фактом. Коротко до 300 символов или не все токены",
        "system": "Ты даёшь проверяемые факты, без воды. Если не уверен — говори об этом.",
        "temperature": 0.4,
        "max_tokens": 200,
    },
    "chat": {
        "developer": "Обычный диалог. Ясно, дружелюбно, без канцелярита.",
        "system": "Ты полезный собеседник.",
        "temperature": 0.7,
        "max_tokens": 800,
    },
    "persona": {
        "developer": "Дальше будет инструкция : ",
        "system": "Говори в выбранной роли. Не выходи из образа, но не нарушай законы и политику.",
        "temperature": 0.8,
        "max_tokens": 800,
    },
    "quiz": {
        "developer": "Следуй инструкции дальше: ",
        "system": "Ты ведущий Quiz придумывай разнообразие вопросы. под ролью ассистент тебе приходят твои старые вопросы не повторяй их",
        "temperature": 0.9,
        "max_tokens": 800,
    },
    "translate": {
        "developer": "Переводи смысл и стиль, без буквального калькирования. Покажи только перевод.",
        "system": "Профессиональный переводчик.",
        "temperature": 0.2,
        "max_tokens": 800,
    },
    "reco": {
        "developer": "Предлагай 3–5 вариантов с короткими пояснениями. Учитывай настроение, жанры и похожесть.",
        "system": "Ты даёшь рекомендации фильмов и книг.",
        "temperature": 0.7,
        "max_tokens": 600,
    },
}


