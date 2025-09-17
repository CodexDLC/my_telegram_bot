import asyncio

import logging

from aiogram import Bot, Dispatcher
from config import BOT_TOKEN
from config_routes import routes

logging.basicConfig(level=logging.INFO)

bot = Bot(BOT_TOKEN)
dp = Dispatcher()

async def main():


    for r in routes:
        dp.include_router(r)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())