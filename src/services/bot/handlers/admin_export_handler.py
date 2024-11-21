from aiogram import F, Router, types, Bot
from aiogram.types import FSInputFile

from src.services.export_excel.services import create_export_file

from src.services.bot.filters.chat_type import ChatTypeFilter, IsAdmin
from logger.logger import setup_logger

export_router = Router(name='export_handler')
export_router.message.filter(ChatTypeFilter(["private"]), IsAdmin())

logger = setup_logger(__name__)


@export_router.message(F.text == 'Выгрузить базу')
async def export_handler(message: types.Message, bot: Bot):
    message = await message.answer("Начинаем экспорт базы данных...")
    try:
        path = await create_export_file()
        if not path.exists():
            logger.error('Файл не найден')
            await message.answer('Файл не найден')
            return

        file = FSInputFile(path)
        await bot.send_document(chat_id=message.chat.id, document=file)
        await message.delete()

    except Exception as e:
        logger.exception(e)
        await message.reply(f'Ошибка экспорта, {e}')
