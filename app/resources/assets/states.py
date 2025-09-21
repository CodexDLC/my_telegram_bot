from aiogram.fsm.state import StatesGroup, State





class ChatGpt(StatesGroup):
    TEXT_MSG = State()
    CONFIRM_GPT = State()