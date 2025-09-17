from aiogram.types import Message, CallbackQuery
from aiogram.exceptions import TelegramBadRequest

# твои функции/константы
from presentation.keyboards.keyboard import start_inline_kb
from presentation.text.start import start_text


# где лежит текст меню


async def show_start_menu(ctx: Message | CallbackQuery) -> None:
    kb = start_inline_kb()

    # вызов из колбэка → редактируем существующее сообщение
    if isinstance(ctx, CallbackQuery):
        await ctx.answer()  # убрать «часики»
        msg = ctx.message

        if msg is None:
            # инлайн-режим (редкость). Тогда нужно через bot.edit_message_text
            await ctx.bot.edit_message_text(
                inline_message_id=ctx.inline_message_id,
                text=start_text,
                parse_mode="HTML",
                reply_markup=kb,
            )
            return

        try:
            # если предыдущее было фото с подписью — меняем подпись
            if msg.photo:
                await msg.edit_caption(
                    caption=start_text, reply_markup=kb, parse_mode="HTML"
                )
            else:
                await msg.edit_text(start_text, reply_markup=kb, parse_mode="HTML")
        except TelegramBadRequest:
            # если "message is not modified" или нельзя редактировать — отправим новое
            await msg.answer(start_text, reply_markup=kb, parse_mode="HTML")

    # вызов из /start → просто отправляем новое
    else:  # Message
        await ctx.answer(start_text, reply_markup=kb, parse_mode="HTML")
