# presentation/keyboards/buttons.py

from aiogram.types import InlineKeyboardButton

# -= Кнопки для start панели =-
btn_create_ad = InlineKeyboardButton(text="Создать", callback_data="adv:create")
btn_list_ads = InlineKeyboardButton(text="Показать список", callback_data="adv:list")
btn_find_ads = InlineKeyboardButton(text="Найти по ключу", callback_data="adv:find")

# Кнопка меню Confirm
btn_confirm = InlineKeyboardButton(text="Сохранить", callback_data="adv:confirm:save")
btn_return = InlineKeyboardButton(text="Назад", callback_data="adv:confirm:back")
btn_cancel = InlineKeyboardButton(text="Отмена", callback_data="adv:confirm:cancel")

