from aiogram import Router
from aiogram.types import Message

router = Router()


# Ловим потерянные сообщения
@router.message()
async def main_message_missed(message: Message):
    await message.answer("Я не понимаю Вас 🤷‍♂️")