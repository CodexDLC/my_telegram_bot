import json
from typing import TypedDict

from app.services.json_sanitizer import extract_json_str


class RecoPayload(TypedDict):
    title: str
    description: str
    rating: list[str]


async def parser_recommendation(data: str) -> tuple[str, str, list[str]]:
    json_str = extract_json_str(data)
    payload: RecoPayload = json.loads(json_str)

    title = payload.get("title")
    description = payload.get("description")
    rating = payload.get("rating")

    if not isinstance(title, str):
        raise ValueError("field 'title' не имеет тип str")
    if not isinstance(description, str):
        raise ValueError("field 'description' не имеет тип str")
    if not isinstance(rating, list) and all(isinstance(x, str) for x in rating):
        raise ValueError("field 'rating' не имеет тип list[str]")



    return title, description, rating