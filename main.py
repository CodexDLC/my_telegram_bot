import asyncio

import logging

from aiogram import Bot, Dispatcher
from config import BOT_TOKEN
from presentation.route.commands import command_router

logging.basicConfig(level=logging.INFO)

bot = Bot(BOT_TOKEN)
dp = Dispatcher()

async def main():

    dp.include_router(command_router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())