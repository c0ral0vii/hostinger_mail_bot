import asyncio
from aiogram import Bot, Dispatcher, F, types

from logger.logger import setup_logger
from config.config import Config
import pathlib


async def run():
    path = pathlib.Path(__file__).parent.resolve()
    settings = Config()
    logger = await setup_logger(path=path.joinpath('logs').resolve(), debug=await settings.get_debug_status())
    logger.info('Инициализация')

    bot = Bot(token=await settings.get_bot_api())
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