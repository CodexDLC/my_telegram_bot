# database/db_contract/i_context_repo.py
from abc import ABC, abstractmethod
from typing import List, Dict, Any

# Создадим псевдоним и для этой "строки"
ContextRow = Dict[str, Any]


class IContextRepo(ABC):

    @abstractmethod
    async def add_context_message(self, user_id: int, mode: str, role: str, content: str) -> None:
        """Добавляет одно сообщение в историю контекста."""
        pass

    @abstractmethod
    async def get_context_history(self, user_id: int, mode: str, limit: int = 10) -> List[ContextRow]:
        """
        Получает 'limit' последних сообщений для конкретного
        пользователя и конкретного режима.
        """
        pass

    @abstractmethod
    async def clear_context_history(self, user_id: int, mode: str) -> None:
        """
        Очищает историю для конкретного пользователя и режима.
        """
        pass