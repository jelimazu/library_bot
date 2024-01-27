from aiogram import Router
from aiogram.filters import ExceptionMessageFilter
from aiogram.handlers import ErrorHandler

from data.config import config

router = Router()


# Ловим ошибки
@router.errors(ExceptionMessageFilter(
    "Telegram server says - Bad Request: message is not modified: specified new message content and reply markup are exactly the same as a current content and reply markup of the message")
)
class MyHandler(ErrorHandler):
    async def handle(self):
        pass


@router.errors()
class MyHandler(ErrorHandler):
    async def handle(self):
        print(self.exception_name)
        print(self.exception_message[self.exception_message.find("exception="):])
        config.logger.service(self.exception_name + " | " + self.exception_message[self.exception_message.find("exception="):])