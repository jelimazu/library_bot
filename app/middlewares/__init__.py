from aiogram import Dispatcher

from app.middlewares.middleware_throttling import ThrottlingMiddleware


# Регистрация всех миддлварей
def register_all_middlewares(dp: Dispatcher):
    dp.message.middleware(ThrottlingMiddleware())