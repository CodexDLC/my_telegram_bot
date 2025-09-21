from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder





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