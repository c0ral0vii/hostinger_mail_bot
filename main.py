import asyncio
from sched import scheduler

import pytz
from aiogram import Bot, Dispatcher, types
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from logger.logger import setup_logger
from config.config import settings
from src.services.bot.handlers import (
    start_handler,
    admin_handler,
    search_handler,
    code_handler,
    admin_search_handler,
    admin_export_handler,
    admin_import_handler,
    admin_add_emails,
    admin_crud_handler,
    admin_export_emails,
    admin_to_next_month_handler,
)
from src.services.database_saver.services import DatabaseSaverService
from src.services.notification.service import Notification

logger = setup_logger(__name__)


async def run():
    # path = pathlib.Path(__file__).parent.resolve()
    logger.info('Инициализация')

    bot = Bot(token=settings.get_bot_api())
    dp = Dispatcher()

    dp.include_routers(
        start_handler.command_router,
        admin_export_emails.admin_export_router,
        admin_crud_handler.admin_crud_router,
        admin_handler.admin_router,
        admin_search_handler.admin_search,
        admin_export_handler.export_router,
        admin_import_handler.admin_import,
        admin_add_emails.add_emails_router,
        admin_to_next_month_handler.to_next_month_router,

        search_handler.search_router,   
        code_handler.get_code_router,
    )

    await on_startup(bot=bot)
    await bot.delete_webhook(drop_pending_updates=True)
    logger.info('Запуск')

    await dp.start_polling(bot)


async def on_startup(bot: Bot):
    notification = Notification(bot=bot)
    database_saver = DatabaseSaverService()
    # await database_saver.start_save() для тестов

    scheduler = AsyncIOScheduler(timezone=pytz.timezone('Europe/Moscow'))
    scheduler.add_job(database_saver.start_save, 'cron', hour=0, minute=0)
    scheduler.add_job(notification.start, 'cron', hour=10, minute=0)
    # scheduler.add_job(notification.start, 'interval', seconds=5) # Для тестов
    
    scheduler.start()


    commands = [
        types.BotCommand(command="/start", description="Запуск бота"),
    ]

    await bot.set_my_commands(commands)


if __name__ == '__main__':
    asyncio.run(run())