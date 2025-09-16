from aiogram.types import ReplyKeyboardMarkup


from presentation.keyboards.buttons import button_announcement, button_list


def start_keyboard():
    return ReplyKeyboardMarkup(keyboard=[button_announcement, button_list])
