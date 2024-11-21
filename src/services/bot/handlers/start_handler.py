from aiogram import types, Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext

from src.services.bot.keyboards.reply.keyboards import create_start_keyboard
from logger.logger import setup_logger


command_router = Router(name='command_handler')
logger = setup_logger(__name__)


@command_router.message(CommandStart())
async def start_handler(message: types.Message, state: FSMContext):
    await state.clear()
    logger.info(fr'Пользователь @{message.from_user.username}, ID {message.from_user.id} - /start')
    await message.answer(f'Привет, ты можешь узнать когда тебе предстоит оплатить \
                                сервис или получить код с почты', reply_markup=create_start_keyboard())