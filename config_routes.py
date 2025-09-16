# config_routes.py
from presentation.route.commands import router as command_router
from presentation.route.callback.start_menu import router as router_create_announcement
from presentation.route.chat import router as router_chat

routes = (
    command_router,
    router_create_announcement,
    router_chat
)