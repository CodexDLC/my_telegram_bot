from aiogram import Router

from .callback.chat_gpt import router as chat_gpt_router
from .callback.persona_chat import router as persona_chat_router
from .callback.quiz import router as quiz_router
from .callback.random_handler import router as random_fact_router
from .callback.translate_talk import router as translate_talk_router
from .callback.universal import router as universal_router
from .callback.recommendation import router as recommendation_router
from .commands import router as command_router
from .setting_callback.model_selection import router as model_setting_router
from .footer_menu import router as footer_menu_router


router = Router()


router.include_routers(
    command_router,
    model_setting_router,
    footer_menu_router,
    chat_gpt_router,
    persona_chat_router,
    translate_talk_router,
    quiz_router,
    random_fact_router,
    recommendation_router,
    universal_router,

)
