#app/resources/assets/states.py


from aiogram.fsm.state import State, StatesGroup


class ChatGpt(StatesGroup):
    TEXT_MSG = State()


class TranslateChat(StatesGroup):
    TEXT_TRANSLATE = State()


class PersonTalk(StatesGroup):
    TEXT_PERSONA = State()



class QuizGame(StatesGroup):
    START_GAME = State()
    PLAYING_GAME = State()



class Recommendations(StatesGroup):
    CHOOSE_CATEGORY = State()
    CHOOSE_GENRE = State()
    SHOW_RECOMMENDATION = State()