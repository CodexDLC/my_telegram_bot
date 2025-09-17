# config_routes.py
from presentation.route.commands import router as command_router
from presentation.route.callback.start_menu import router as router_create_announcement
from presentation.route.chat import router as router_chat
from presentation.route.FSM.add_fsm import router as add_fsm_router

routes = (
    command_router,
    router_create_announcement,
    add_fsm_router,
    router_chat
)