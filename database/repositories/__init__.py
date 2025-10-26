# database/repositories/__init__.py
import aiosqlite
from database.db_contract.i_user_repo import IUserRepo
from .SQLite.user_repo import SQLiteUserRepo

# Вот наша "Фабрика"
def get_user_repo(db: aiosqlite.Connection) -> IUserRepo:
    """
    Эта функция - ЕДИНСТВЕННОЕ место, которое знает,
    какую реализацию IUserRepo мы используем.
    """
    # Сейчас мы жестко возвращаем SQLite-реализацию
    return SQLiteUserRepo(db)


