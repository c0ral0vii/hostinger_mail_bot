from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from src.services.bot.filters.chat_type import ChatTypeFilter, IsAdmin
from src.services.bot.keyboards.reply import admin_keyboard
from logger.logger import setup_logger


admin_router = Router(name='admin_router')
admin_router.message.filter(ChatTypeFilter(["private"]), IsAdmin())

logger = setup_logger(__name__)

@admin_router.message(Command('admin'))
async def start_admin(message: types.Message, state: FSMContext):
    logger.info(f'Пользователь вошёл в админ панель - @{message.from_user.username}, ID: {message.from_user.id}')
    await state.clear()
    await message.answer(f'Вы вошли в админ панель', reply_markup=admin_keyboard.create_admin_keyboard())
