
import asyncio
from app.core.log_setup import setup_logging
setup_logging(level="DEBUG", to_file=True)
import logging

from app.core.bot_factory import build_app
from app.core.config import BOT_TOKEN





async def main():
    log = logging.getLogger(__name__)
    bot, dp = build_app(BOT_TOKEN)


    log.info("Бот стартует")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
