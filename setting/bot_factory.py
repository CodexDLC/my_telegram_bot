# setting/bot_factory.py

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

def build_app(token: str):
    """

    :param token: Token бота
    :return: объект бота телеграмма и диспетчер
    """
    bot = Bot(token)
    dp = Dispatcher(storage=MemoryStorage())
    return bot, dp
