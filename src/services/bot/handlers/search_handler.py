from aiogram import Router, types, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

from logger.logger import setup_logger
from src.services.bot.fsm.user_states import InputNumberState
from src.services.bot.keyboards.inline.code_keyboard import get_code_kb
from src.services.database.orm.users import search_user
from src.services.database.orm.everyday_message import create_everyday_message


search_router = Router(name="search_router")

logger = setup_logger(__name__)


@search_router.message(F.text == "Найти в базе")
async def search(message: types.Message, state: FSMContext):
    """Поиск по базе"""

    logger.info(fr'Начал поиск - @{message.from_user.username}, ID: {message.from_user.id}')
    await state.set_state(InputNumberState.number)
    await message.answer('Введите определённый номер')


@search_router.message(F.text, StateFilter(InputNumberState.number))
async def search(message: types.Message, state: FSMContext):
    await state.update_data(number=message.text)
    data = await state.get_data()
    cross_number = data['number']

    info = await search_user(serial_number=str(cross_number).strip().upper())

    if info.get('error'):
        logger.critical(f"ID-{message.from_user.id}, @{message.from_user.username}---{info.get('error')}, {info.get('text')}")
        await message.answer(f"{info.get('error')}. {info.get('text')}")
    else:
        day_message = await create_everyday_message()
        await message.answer(f'По данному серийному номеру({cross_number}) было найдено\nДень до которого необходимо оплатить - {info.get('pay_date')}\nВаш логин - {info.get('email')}\nВаш пароль - {info.get("password")}\n\nСообщение дня: {"-" if day_message.message is None else day_message.message}',
                             reply_markup=get_code_kb(cross_number=cross_number, user=True))
        await state.clear()