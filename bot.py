import os
import asyncio
from loguru import logger
from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from app.handlers.registration import register_user_registration_handlers
from app.handlers.base import register_base_handlers
from app.handlers.send_video import register_send_video_handlers
from dotenv import load_dotenv


logger.add(os.getcwd() + '/logs/debug.log', level='DEBUG', rotation='00:00', compression='zip')

load_dotenv()
API_TOKEN = os.getenv('API_TOKEN')


async def set_commands(bot: Bot):
    """Меню команд"""

    commands = [
        BotCommand(command="/start", description="Старт"),
        BotCommand(command="/register", description="Регистрация"),
        BotCommand(command="/video", description="Отправить видео"),
        BotCommand(command="/cancel", description="Отменить"),
    ]
    await bot.set_my_commands(commands)


async def main():

    bot = Bot(token=API_TOKEN)
    dp = Dispatcher(bot, storage=MemoryStorage())  # TODO: перенести на redis
    register_base_handlers(dp)  # базовые команды бота
    register_user_registration_handlers(dp)  # регистрация пользователя
    register_send_video_handlers(dp)  # отправка видео
    await set_commands(bot)  # доступные команды (в чате бота)
    await dp.start_polling()  # TODO: для локального использования. Необходимо сменить для прод.


if __name__ == '__main__':
    asyncio.run(main())
