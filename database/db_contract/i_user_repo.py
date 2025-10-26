# database/db_contract/i_user_repo.py
from abc import ABC, abstractmethod
from typing import Optional, List, Dict, Any

# Мы будем ожидать, что методы возвращают dict-like объекты
# (aiosqlite.Row идеально подходит)
UserRow = Dict[str, Any]


class IUserRepo(ABC):

    @abstractmethod
    async def upsert_user(self, user_id: int, first_name: str, username: Optional[str]) -> None:
        """ 
        Добавляет пользователя, если его нет (для /start).
        Если есть - может обновить username.
        """
        pass

    @abstractmethod
    async def get_user(self, user_id: int) -> Optional[UserRow]:
        """
        Получает ВСЮ информацию о пользователе (всю строку).
        """
        pass

    @abstractmethod
    async def update_user_model(self, user_id: int, model_name: str) -> None:
        """
        Точечно обновляет ТОЛЬКО модель LLM для пользователя.
        """
        pass

    @abstractmethod
    async def update_user_language(self, user_id: int, lang_code: str) -> None:
        """
        Точечно обновляет ТОЛЬКО язык пользователя.
        """
        pass

    # Эти методы пока не нужны, но хорошо, что ты о них подумал
    @abstractmethod
    async def get_all_users(self) -> List[UserRow]:
        pass

    @abstractmethod
    async def delete_user(self, user_id: int) -> None:
        pass