# app/resources/keyboards/reply.py
from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder

btn_footer_menu = "🏠 Меню"
btn_footer_help = "❓ Помощь"
btn_footer_setting = "⚙️ Настройки"


def main_kb() -> ReplyKeyboardMarkup:
    b = ReplyKeyboardBuilder()
    b.button(text=btn_footer_menu)
    b.button(text=btn_footer_help)
    b.button(text=btn_footer_setting)
    b.adjust(2)
    return b.as_markup(
        resize_keyboard=True,
        one_time_keyboard=False,
        is_persistent=True,
        input_field_placeholder="Основные действия",
    )
