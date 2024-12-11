from aiogram import Router, F, types
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

from src.services.bot.fsm.user_states import InputNumberState
from src.services.bot.keyboards.inline.code_keyboard import get_code_kb
from src.services.database.orm.users import get_user_admin

from src.services.bot.filters.chat_type import ChatTypeFilter, IsAdmin
from logger.logger import setup_logger

admin_search = Router(name='admin_search')
admin_search.message.filter(ChatTypeFilter(["private"]), IsAdmin())

logger = setup_logger(__name__)


@admin_search.message(F.text == 'Найти в базе(админ)')
async def search_user(message: types.Message, state: FSMContext):
    """Поиск по базе"""

    logger.info(fr'Начал поиск - @{message.from_user.username}, ID: {message.from_user.id}')
    await state.set_state(InputNumberState.number)
    await message.answer('Введите определённый номер или номер телефона')


@admin_search.message(F.text, StateFilter(InputNumberState.number))
async def search(message: types.Message, state: FSMContext):
    await state.update_data(number=message.text)
    data = await state.get_data()
    cross_number = data['number']

    info = await get_user_admin(find_str=str(cross_number).upper())

    if info.get('error'):
        logger.critical(
            f"ID-{message.from_user.id}, @{message.from_user.username}---{info.get('error')}, {info.get('text')}")
        await message.answer(f"{info.get('error')}. {info.get('text')}")
    else:
        await message.answer(
            f'👱{info.get("user_id")}\n🤖Серийный номер: {info.get("serial_number")}\n📅Дата оплаты: {info.get("need_pay_date")}\n🤖Статус паузы: {"На паузе" if info.get("stay_on_pause") else "Активен"}\n🤖Юзернейм: {info.get("username")}\n✉️Логин: {info.get("email")}\n🤖Пароль: {info.get("password")}\n📞Номер телефона {info.get("phone")}\n\nКоментарий: {info.get("comment", "Не указан")}',
            reply_markup=get_code_kb(cross_number=cross_number))
        await state.clear()