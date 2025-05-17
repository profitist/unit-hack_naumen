from aiogram import Dispatcher
from app.handlers.user_handlers import user_router
from app.handlers.admin_handlers import admin_router


def register_all_handlers(dp: Dispatcher):
    dp.include_router(user_router)
    dp.include_router(admin_router)
