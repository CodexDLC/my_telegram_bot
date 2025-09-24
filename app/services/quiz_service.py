import logging
import json
from html import escape
from typing import Any, Coroutine

from app.resources.assets.quiz_theme import DIFFICULTY_DATA
from app.resources.keyboards.inline import quiz_question_inline_kb

log = logging.getLogger(__name__)


async def parser_question(data)->tuple:
    data = json.loads(data)
    print(f"{type(data)} - {data}")
    kb_data = data['options']
    question_resp_index = data['correct']
    question_resp_text = data['explanation']

    text_quest = f"""    
    <b>Вопрос:</b> {data.get('question')}        
    """
    kb = quiz_question_inline_kb(kb_data)

    return (text_quest, question_resp_index, question_resp_text,
            kb)


def make_ui_quiz(data: dict) -> str:
    score  = data.get("score_game", 0)
    round_ = data.get("score_round", 1)
    label  = escape(str(data["label"]))
    topic = escape(str(data.get("topic")))

    txt = (f"""\
        <b>Очки:</b> {score}, <b>Сложность:</b> -={label}=-
        <b>Раунд:</b> {round_}, <b>Тема игры:</b> {topic}.
    """).strip()
    return txt


async def summ_score(dif: str, score: int) -> int | None:
    """

    :param dif: Сложность
    :param score: текущие очки в игре
    :return: очки после верного угадывания вопроса
    """

    for key, data in DIFFICULTY_DATA.items():
        if dif == key:
            add_score = data["score"]
            score += add_score
            return score
    return None


