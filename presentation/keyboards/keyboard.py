# presentation/keyboards/keyboard.py

from aiogram.types import InlineKeyboardMarkup
from presentation.keyboards.buttons import (
    btn_create_ad,
    btn_list_ads,
    btn_find_ads,
    btn_confirm,
    btn_return,
    btn_cancel,
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
