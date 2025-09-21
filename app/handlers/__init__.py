from aiogram import Router

from .commands import router as command_router
from .footer_menu import router as footer_menu_router
from .callback.random_handler import router as random_fact_router
from .callback.universal import router as universal_router



router = Router()


router.include_routers(command_router, footer_menu_router, random_fact_router, universal_router)