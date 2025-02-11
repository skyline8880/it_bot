from aiogram import Router

from handlers.commands import router as command_router

router = Router()

router.include_routers(
    command_router
)
