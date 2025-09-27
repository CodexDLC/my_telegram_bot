import json
import logging
from html import escape
from typing import List, TypedDict

from aiogram.types import InlineKeyboardMarkup

from app.resources.assets.quiz_theme import DIFFICULTY_DATA
from app.resources.keyboards.inline import quiz_question_inline_kb

log = logging.getLogger(__name__)


class QuizPayload(TypedDict):
    question: str
    options: List[str]     # или list[str], если Python 3.9+
    correct: int
    explanation: str

async def parser_question(data: str) -> tuple[str, int, str, str, InlineKeyboardMarkup]:
    payload: QuizPayload = json.loads(data)  # <-- теперь это dict с нужными ключами

    kb_data = payload.get('options')
    question_resp_index = payload.get('correct')
    question_resp_text = payload.get('explanation')
    clearn_question = payload.get('question')

    if not isinstance(clearn_question, str):
        raise ValueError("field 'question' не имеет тип str")
    if not (isinstance(kb_data, list) and all(isinstance(x, str) for x in kb_data)):
        raise ValueError("field 'options' не имеет тип list[str]")
    if not isinstance(question_resp_index, int):
        raise ValueError("field 'correct' не имеет тип int")
    if not isinstance(question_resp_text, str):
        raise ValueError("field 'explanation' не имеет тип str")

    text_quest = f"""    
    <b>Вопрос:</b> {clearn_question}        
    """
    kb = quiz_question_inline_kb(kb_data)

    return (text_quest,
            question_resp_index,
            question_resp_text,
            clearn_question, kb)


def make_ui_quiz(data: dict[str, int]) -> str:
    score  = data.get("score_game", 0)
    round_ = data.get("score_round", 1)
    label  = escape(str(data["label"]))
    topic = escape(str(data.get("topic")))

    txt = (f"""\
        <b>Очки:</b> {score}, <b>Сложность:</b> -={label}=-
        <b>Раунд:</b> {round_}, <b>Тема игры:</b> {topic}.
    """).strip()
    return txt


async def summ_score(dif: str, score: int) -> int:
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
    return 0



# async def