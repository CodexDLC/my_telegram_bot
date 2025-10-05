# app/resources/keyboards/inline.py
import logging

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.resources.assets.quiz_theme import QUIZ_THEME
from app.resources.assets.recommen_dict import RECO_CATEGORIES
from app.resources.assets.role_dict import ROLE_SPECS
from app.resources.assets.translite_dict import lang
from app.services.llm_provider import LLM_SERVICES

log = logging.getLogger(__name__)

btn_main_menu = InlineKeyboardButton(
    text="🔙 Вернуться в меню",
    callback_data="main_menu",
)

def start_inline_kb() -> InlineKeyboardMarkup:
    """
    :return: Возврат стартовой клавиатуры с 6 основными режимами.
    """
    kb = InlineKeyboardBuilder()
    kb.button(text="🎲 Рандомный факт", callback_data="fact_random")
    kb.button(text="🤖 ChatGPT интерфейс", callback_data="ui_chatgpt")
    kb.button(text="👥🗣️ Диалог с личностью", callback_data="dialog_persona")
    kb.button(text="❓ Квиз", callback_data="quiz_open")
    kb.button(text="🌐 Переводчик", callback_data="translate_open")
    kb.button(text="🎬 Рекомендации", callback_data="reco_open")
    kb.adjust(2)

    return kb.as_markup()



def setting_menu_inline_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text="Выбор модели", callback_data="model_selection")


    return kb.as_markup()

def setting_model_selection_inline_kb(*arg) -> InlineKeyboardMarkup:
    """
    :return: Возврат клавиатуры выбора модели.
    """
    model = arg[0] if arg else None
    kb = InlineKeyboardBuilder()
    for key in LLM_SERVICES.keys():
        if model == key:
            kb.button(text=f"✅ Модель: {key}", callback_data=f"model:{key}")
        else:
            kb.button(text=f"🤖 Модель: {key}", callback_data=f"model:{key}")
    kb.adjust(2)
    kb.row(btn_main_menu)
    return kb.as_markup()


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
    :return: Клавиатура для общения с ботом чат гпт.

    """
    kb = InlineKeyboardBuilder()
    kb.add(btn_main_menu)
    kb.adjust(1)

    return kb.as_markup()


def translate_inline_kb(*args) -> InlineKeyboardMarkup:
    """
    :return: Клавиатура для выбора языка перевода.

    """
    choice = args[0] if args else None

    kb = InlineKeyboardBuilder()
    for key, value in lang.items():
        if key == choice:
            kb.button(text=f"✅ {value}", callback_data=f"tlang:{key}")
        else:
            kb.button(text=value, callback_data=f"tlang:{key}")
    kb.adjust(3)
    kb.row(btn_main_menu)
    return kb.as_markup()

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


def quiz_question_inline_kb(data: list[str])-> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()

    for i, value in enumerate(data):
        kb.button(text=value, callback_data=f"index:{i}")
    kb.adjust(2)

    return kb.as_markup()


def recommend_inline_kb()->InlineKeyboardMarkup:
    """

    :return: Клавиатура с выбором типа рекомендации
    """
    kb = InlineKeyboardBuilder()
    kb.button(text="🎥 Фильмы", callback_data="reco_category:movies")
    kb.button(text="🎞️ Сериалы", callback_data="reco_category:series")
    kb.button(text="🎦 Аниме", callback_data="reco_category:anime")
    kb.button(text="📖 Книги", callback_data="reco_category:books")
    kb.add(btn_main_menu)
    kb.adjust(2)

    return kb.as_markup()


def genre_inline_kb(category: str, apply: set[str])->InlineKeyboardMarkup:
    key_category = RECO_CATEGORIES.get(category)
    kb = InlineKeyboardBuilder()
    bottom_buttons = []
    for key, value in key_category.items():
        log.debug(f"Ключ = {key}, подпись = {value}")
        if key in apply:
            kb.button(text=f"✅ {value}", callback_data=f"genre:{key}")
        else:
            kb.button(text=value, callback_data=f"genre:{key}")
    kb.adjust(3)
    if apply:
        btn_confirm = InlineKeyboardButton(text="Подобрать", callback_data="reco:confirm")
        bottom_buttons.append(btn_confirm)  # Добавляем ее в наш список

    bottom_buttons.append(btn_main_menu)

    kb.row(*bottom_buttons)

    return kb.as_markup()


def confirm_reco_inline_kb()->InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text="🎞️ Еще рекомендацию", callback_data="reco:restart")
    kb.button(text="🆕 Сменить категорию", callback_data="reco_open")
    kb.add(btn_main_menu)
    kb.adjust(2)

    return kb.as_markup()


