import asyncio
import logging

from app.core.bot_factory import build_app
from app.core.config import BOT_TOKEN
from app.core.log_setup import setup_logging
from app.handlers import router

setup_logging(level="DEBUG", to_file=True)


async def main()-> None:
    log = logging.getLogger(__name__)
    if BOT_TOKEN is not None:
        bot, dp = build_app(token=BOT_TOKEN)
        dp.include_router(router)
        log.info("Бот стартует")
        await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
