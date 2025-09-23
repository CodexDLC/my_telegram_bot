from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.resources.assets.dict_preset import ROLE_SPECS


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




def get_person_inline_kb() -> InlineKeyboardMarkup:

    rows = [[InlineKeyboardButton(text=spec["label"], callback_data=f"ROLE:{key}")]
            for key, spec in ROLE_SPECS.items()]
    return InlineKeyboardMarkup(inline_keyboard=rows)

def person_inline_kb() -> InlineKeyboardMarkup:
    """
    :return: Клавиатура для меню общения с возможностью выйти или изменить собеседника

    """
    kb = InlineKeyboardBuilder()
    kb.button(text="Новая личность", callback_data="switch_role")
    kb.add(btn_main_menu)
    kb.adjust(2)

    return kb.as_markup()