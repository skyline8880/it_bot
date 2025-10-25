from aiogram import Router

from handlers.commands import router as command_router
from handlers.request import router as request_router
from handlers.admin import router as admin_router

router = Router()

router.include_routers(
    command_router,
    request_router,
    admin_router
)
