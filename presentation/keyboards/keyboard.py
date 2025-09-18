# presentation/keyboards/keyboard.py

from aiogram.types import InlineKeyboardMarkup, ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from constant.F_text_menu import kb_maine_ad, kb_maine_hide, kb_maine_help
from presentation.keyboards.buttons import (
    btn_create_ad, btn_list_ads, btn_find_ads,
    btn_confirm, btn_return, btn_cancel
)


def main_kb() -> ReplyKeyboardMarkup:
    b = ReplyKeyboardBuilder()
    b.button(text=kb_maine_ad)
    b.button(text=kb_maine_hide)
    b.button(text=kb_maine_help)
    b.adjust(1, 2)
    return b.as_markup(
        resize_keyboard=True,
        one_time_keyboard=False,
        is_persistent=True,
        input_field_placeholder="Основные действия",
    )



def start_inline_kb() -> InlineKeyboardMarkup:
    # раскладка: по одной кнопке в ряд
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [btn_create_ad],
            [btn_list_ads],
            [btn_find_ads],
        ]
    )


def confirm_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [btn_confirm],
            [btn_return],
            [btn_cancel],
        ]
    )



