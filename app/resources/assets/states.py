from aiogram.fsm.state import StatesGroup, State





class ChatGpt(StatesGroup):
    TEXT_MSG = State()



class TranslateChat(StatesGroup):
    TEXT_TRANSLATE = State()


class PersonTalk(StatesGroup):
    TEXT_PERSONA = State()