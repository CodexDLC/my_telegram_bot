from typing import TypedDict, Literal, Final, get_args

ThemeKey = Literal["sport", "history", "science", "python"]
Difficulty = Literal["easy", "normal", "hard", "impossible"]

ALL_DIFFICULTIES: tuple[Difficulty, ...] = get_args(Difficulty)

class DifficultyData(TypedDict):
    label: str
    score: int

class QuizTheme(TypedDict):
    label: str
    descriptions: str


DIFFICULTY_DATA: Final[dict[Difficulty, DifficultyData]] = {
    "easy" : {
        "label" : "Легкая",
        "score" : 1
    },
    "normal" : {
        "label" : "Средняя",
        "score" : 2
    },
    "hard": {
        "label" : "Сложная",
        "score": 5
    },
    "impossible": {
        "label" : "Невозможная",
        "score": 10
    }
}

game_rules = f"""

Игра идет до 100 очков. Каждые несколько раундов повышается сложность игры.

В зависимости от сложности очки прибавляются по разному.

easy = 1 
normal = 2 
hard = 5
impossible =10

"""


QUIZ_THEME: Final[dict[ThemeKey, QuizTheme]]  = {

    "sport" : {
        "label" : "⚽ Спорт",
        "descriptions" : f"{game_rules}."
    },
    "history": {
        "label": "📜 История",
        "descriptions" : f"{game_rules}."
    },

    "science": {
        "label": "🧑‍🔬 Наука",
        "descriptions" : f"{game_rules}."
    },

    "python": {
        "label": "🔢 Python",
        "descriptions" : f"{game_rules}."
    },
}



TOPIC_KEYS = set(QUIZ_THEME.keys())

DEV_SQUIZ = """
Твоя задача — сгенерировать НОВЫЙ, УНИКАЛЬНЫЙ вопрос для викторины, которого еще не было.
Ответ — строго JSON-объект без каких-либо пояснений/текста вне JSON.
Схема полей: question (str ≤ 500), options (list[str], 4, уникальные), 
correct (int, 0-индексация), explanation (str ≤ 300).
Никакого Markdown, кавычек-кодов и текста вне JSON. Только JSON.
Вопросы на русском языке
Если данных мало — делай общий, но корректный вопрос.

"""





