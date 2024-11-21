import asyncio
from aiogram import Bot, Dispatcher, types

from logger.logger import setup_logger
from config.config import settings
from src.services.bot.handlers import (
    start_handler,
    admin_handler,
    search_handler,
    code_handler,
    admin_search_handler,
    admin_export_handler,
)
import pathlib

logger = setup_logger(__name__)

async def run():
    # path = pathlib.Path(__file__).parent.resolve()
    logger.info('Инициализация')

    bot = Bot(token=settings.get_bot_api())
    dp = Dispatcher()

    dp.include_routers(
        start_handler.command_router,
        admin_handler.admin_router,
        admin_search_handler.admin_search,
        admin_export_handler.export_router,
        search_handler.search_router,
        code_handler.get_code_router,
    )

    await on_startup(bot=bot)
    await bot.delete_webhook(drop_pending_updates=True)
    logger.info('Запуск')

    await dp.start_polling(bot)


async def on_startup(bot: Bot):
    commands = [
        types.BotCommand(command="/start", description="Запуск бота"),
    ]

    await bot.set_my_commands(commands)


if __name__ == '__main__':
    asyncio.run(run())