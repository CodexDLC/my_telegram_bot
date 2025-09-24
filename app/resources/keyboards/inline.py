# app/resources/keyboards/inline.py
import logging

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


from app.resources.assets.quiz_theme import QUIZ_THEME
from app.resources.assets.role_dict import ROLE_SPECS

log = logging.getLogger(__name__)

def start_inline_kb() -> InlineKeyboardMarkup:
    """
    :return: Возврат стартовой клавиатуры с 6 основными режимами.
    """
    kb = InlineKeyboardBuilder()
    kb.button(text="🎲 Рандомный факт", callback_data="fact_random")
    kb.button(text="🤖 ChatGPT интерфейс", callback_data="ui_chatgpt")
    kb.button(text="🗣️ Диалог с личностью", callback_data="dialog_persona")
    kb.button(text="❓ Квиз", callback_data="quiz_open")
    kb.button(text="🌐 Переводчик", callback_data="translate_open")
    kb.button(text="🎬 Рекомендации", callback_data="recs_open")
    kb.adjust(2)

    return kb.as_markup()


btn_main_menu = InlineKeyboardButton(
    text="🔙 Вернуться в меню",
    callback_data="main_menu",
)


def random_inline_kb() -> InlineKeyboardMarkup:
    """
    :return: Возврат клавиатуры в меню рандом факт. Повторить факт или вернуться в главное меню
    """
    kb = InlineKeyboardBuilder()
    kb.button(text="🎲 Еще факт", callback_data="fact_random")
    kb.add(btn_main_menu)
    kb.adjust(2)
    return kb.as_markup()


def chat_inline_kb() -> InlineKeyboardMarkup:
    """
    :return: Клавиатура для общения с ботом чат гпт .

    """
    kb = InlineKeyboardBuilder()
    kb.add(btn_main_menu)
    kb.adjust(1)

    return kb.as_markup()


def translate_inline_kb() -> InlineKeyboardMarkup:
    """
    :return: Клавиатура для выбора языка перевода.

    """

    kb = InlineKeyboardBuilder()
    kb.button(text="Британский", callback_data="tlang:en")
    kb.button(text="Немецкий", callback_data="tlang:de")
    kb.button(text="Французский", callback_data="tlang:fr")
    kb.add(btn_main_menu)
    kb.adjust(3)

    return kb.as_markup()

# в теории можно сделать одну универсальную клавиатуру для нескольких режимов, которые принимаю Dict
# Но я пока не хочу заморачиваться переписывать код. Потом может улучшу
def get_person_inline_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    for key, spec in ROLE_SPECS.items():
        kb.button(text=spec["label"], callback_data=f"ROLE:{key}")

    kb.add(btn_main_menu)
    kb.adjust(2)
    return kb.as_markup()


def person_inline_kb() -> InlineKeyboardMarkup:
    """
    :return: Клавиатура для меню общения с возможностью выйти или изменить собеседника

    """
    kb = InlineKeyboardBuilder()
    kb.button(text="Новая личность", callback_data="switch_role")
    kb.add(btn_main_menu)
    kb.adjust(2)

    return kb.as_markup()



def get_theme_quiz_inline_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    for key, spec in QUIZ_THEME.items():
        log.debug(f"Ключ = {key}, подпись = {spec["label"]}")
        kb.button(text=spec["label"], callback_data=f"theme:{key}")
    kb.add(btn_main_menu)
    kb.adjust(2)
    return kb.as_markup()

def star_game_inline_kb() -> InlineKeyboardMarkup:
    """
    :return: Клавиатура старта игры

    """
    kb = InlineKeyboardBuilder()
    kb.button(text="Получить вопрос", callback_data="game:start")
    kb.button(text="Закончить игру", callback_data="game:finish")
    kb.adjust(2)

    return kb.as_markup()


def quiz_question_inline_kb(data: list)-> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    for i, value in enumerate(data):
        kb.button(text=value, callback_data=f"index:{i}")
    kb.adjust(2)
    return kb.as_markup()
