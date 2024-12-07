from aiogram import Router, F, types, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile

from logger.logger import setup_logger
from src.services.bot.filters.chat_type import ChatTypeFilter, IsAdmin
from src.services.export_excel.services import create_export_file_emails

admin_export_router = Router(name='admin_export_emails')
admin_export_router.message.filter(ChatTypeFilter(["private"]), IsAdmin())

logger = setup_logger(__name__)


@admin_export_router.message(F.text == "Выгрузить почты")
async def admin_export_emails(message: types.Message, state: FSMContext, bot: Bot):
    message = await message.answer("Начинаем экспорт базы данных...")
    try:
        path = await create_export_file_emails()
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