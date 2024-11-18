import asyncio
from aiogram import Bot, Dispatcher, types

from logger.logger import setup_logger
from config.config import settings
import pathlib


async def run():
    path = pathlib.Path(__file__).parent.resolve()
    logger = await setup_logger(path=path.joinpath('logs').resolve(), debug=settings.get_debug_status())
    logger.info('Инициализация')

    bot = Bot(token=settings.get_bot_api())
    dp = Dispatcher()

    # dp.include_routers(
    #
    # )

    await on_startup(bot=bot)
    await bot.delete_webhook(drop_pending_updates=True)
    logger.info('Запуск')

    await dp.start_polling(bot)


async def on_startup(bot: Bot):
    commands = [
        types.BotCommand(command="/start", description="Запуск бота"),
        types.BotCommand(command="/help", description="Помощь"),
    ]

    await bot.set_my_commands(commands)


if __name__ == '__main__':
    asyncio.run(run())