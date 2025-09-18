
import asyncio
from setting.log_setup import setup_logging
setup_logging(level="DEBUG", to_file=True)
import logging

from setting.bot_factory import build_app
from setting.config import BOT_TOKEN


from presentation.config_routes import routes




async def main():
    log = logging.getLogger(__name__)

    bot, dp = build_app(BOT_TOKEN)
    for r in routes:
        dp.include_router(r)

    log.info("Бот стартует")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
