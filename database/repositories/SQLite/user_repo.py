# database/repositories/SQLite/user_repo.py
import logging
from typing import Optional, List

import aiosqlite

from database.db_contract.i_user_repo import IUserRepo, UserRow

log = logging.getLogger(__name__)


class SQLiteUserRepo(IUserRepo):
    """
    Репозиторий для работы КРУДС с таблице users
    """
    def __init__(self, db: aiosqlite.Connection):
        self.db = db


    async def upsert_user(self, user_id: int, first_name: str, username: Optional[str]) -> None:
        """
        Добавляет пользователя, если его нет (для /start).
        Если есть - может обновить username.
        """
        sql = """
            INSERT INTO users (user_id, first_name, username) VALUES (?, ?, ?) 
            ON CONFLICT (user_id) 
            DO UPDATE SET username = excluded.username
        """
        await self.db.execute(sql, (user_id, first_name, username))
        log.info(f"Пользователь: {user_id} успешно добавлен в базу данных")



    async def get_user(self, user_id: int) -> Optional[UserRow]:
        """
        Получает ВСЮ информацию о пользователе (всю строку).
        """
        sql = "SELECT * FROM users WHERE user_id = ?"
        async with self.db.execute(sql, (user_id,)) as cursor:
            return await cursor.fetchone()

    async def update_user_model(self, user_id: int, model_name: str) -> None:
        """
        Точечно обновляет ТОЛЬКО модель LLM для пользователя.
        """
        sql = "UPDATE users SET llm_model = ? WHERE user_id = ?"
        await self.db.execute(sql, (model_name, user_id))

    async def update_user_language(self, user_id: int, lang_code: str) -> None:
        """
        Точечно обновляет ТОЛЬКО язык пользователя.
        """
        sql = "UPDATE users SET language_code = ? WHERE user_id =?"
        await self.db.execute(sql, (lang_code, user_id))

    async def get_all_users(self) -> List[UserRow]:
        """
        Возвращает список всех пользователей.
        """
        sql = "SELECT * FROM users"
        async with self.db.execute(sql) as cursor:
            return await cursor.fetchall()

    async def delete_user(self, user_id: int) -> None:
        """
        Удаляет пользователя из базы данных.
        """
        sql = "DELETE FROM users WHERE user_id = ?"
        await self.db.execute(sql, (user_id,))

