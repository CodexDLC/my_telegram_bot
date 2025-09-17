from abc import ABC, abstractmethod
from typing import Any


class IFileAdvRepo(ABC):

    async def save_adv_data(self) -> Any:
        """
        получает данные из state: FSMContext in File or dataBase

        передать данные
        """
        pass
