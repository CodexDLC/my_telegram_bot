from abc import ABC, abstractmethod
from typing import Any


class IFileAdvRepo(ABC):
    @abstractmethod
    async def save_adv_data(self, draft: Any) -> Any:

        """
        получает данные из state: FSMContext in File or dataBase

        передать данные
        """
        pass