from aiogram import Router, types, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

from logger.logger import setup_logger
from src.services.bot.fsm.user_states import InputNumberState
from src.services.database.orm.users import search_user


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

    info = await search_user(serial_number=str(cross_number))

    if info.get('error'):
        logger.critical(f"ID-{message.from_user.id}, @{message.from_user.username}---{info.get('error')}, {info.get('text')}")
        await message.answer(f"{info.get('error')}. {info.get('text')}")
    else:
        await message.answer(f'По данному серийному номеру({cross_number}) было найдено\nДень в который необходимо оплатить - {info.get('pay_date')}\nВаша почта - {info.get('email')}')
        await state.clear()