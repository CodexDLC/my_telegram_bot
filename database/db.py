# В твоем файле db.py
import logging
import aiosqlite
from contextlib import asynccontextmanager

log = logging.getLogger(__name__)

DB_NAME = 'my_bot_db.db'


@asynccontextmanager
async def get_db_connection():
    """
    "Функция-активатор".
    Открывает -> Настраивает -> Отдает -> Закрывает соединение.
    """
    db = None
    try:
        # 1. Подключаемся
        db = await aiosqlite.connect(DB_NAME)

        # 2. Настраиваем Row Factory
        db.row_factory = aiosqlite.Row

        # 3. АКТИВИРУЕМ FOREIGN KEYS
        await db.execute("PRAGMA foreign_keys = ON;")

        # 4. "Отдаем" настроенное соединение в блок 'async with'
        yield db

    except aiosqlite.Error as e:
        log.error(f"Ошибка при работе с БД: {e}")
        # (в реальном коде здесь бы был logging)

    finally:
        # 5. Гарантированно закрываем соединение
        if db:
            await db.close()
