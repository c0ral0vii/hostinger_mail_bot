import datetime

from aiogram import Router, F, types
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from src.services.bot.fsm.user_states import InputNumberState
from src.services.bot.keyboards.inline.code_keyboard import get_code_kb
from src.services.database.orm.crud_users import (
    change_nickname,
    change_pause as change_pause_db,
    change_comment as change_comment_db,
    change_password as change_password_db,
    change_login as change_login_db,
)
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
            f'👱{info.get("user_id")}\n🤖Серийный номер: {info.get("serial_number")}\n📅Дата оплаты: {info.get("pay_date")}\n🤖Статус паузы: {"На паузе" if info.get("stay_on_pause") is True else "Активен"}\n🤖Юзернейм: {info.get("username")}\n✉️Логин: {info.get("email")}\n🤖Пароль: {info.get("password")}\n📞Номер телефона: {info.get("phone")}\n\nКоментарий: {info.get("comment", "Не указан")}',
            reply_markup=get_code_kb(cross_number=cross_number))
        await state.clear()


class ChangeState(StatesGroup):
    new_value = State()


@admin_search.callback_query(F.data.startswith("settings_"))
async def settings(callback: types.CallbackQuery, state: FSMContext):
    serial_number = callback.data.split("_")[-1]

    await callback.message.answer("Что хотите изменить?",
                                  reply_markup=InlineKeyboardMarkup(
                                      inline_keyboard=[
                                          [InlineKeyboardButton(text="📅Изменить дату оплаты",
                                                                callback_data=f"invoice_{serial_number}")],
                                          [InlineKeyboardButton(text="🤖Изменить статус паузы",
                                                                callback_data=f"pause_{serial_number}")],
                                          [InlineKeyboardButton(text="🤖Изменить юзернейм",
                                                                callback_data=f"username_{serial_number}")],
                                          [InlineKeyboardButton(text="✉️Изменить логин",
                                                                callback_data=f"login_{serial_number}")],
                                          [InlineKeyboardButton(text="🤖Изменить пароль",
                                                                callback_data=f"password_{serial_number}")],
                                          [InlineKeyboardButton(text="Изменить коментарий",
                                                                callback_data=f"comment_{serial_number}")],

                                      ]
                                  ))


@admin_search.callback_query(F.data.startswith("invoice_"))
async def change_invoice(callback: types.CallbackQuery, state: FSMContext):
    serial_number = callback.data.split("_")[-1]
    await callback.message.answer(f"Введите новую дату оплаты для устройства с серийным номером {serial_number}:")
    await state.set_state(ChangeState.new_value)
    await state.update_data(serial_number=serial_number, field="invoice")


# Обработка нажатия кнопки "Изменить статус паузы"
@admin_search.callback_query(F.data.startswith("pause_"))
async def change_pause(callback: types.CallbackQuery, state: FSMContext):
    serial_number = callback.data.split("_")[-1]
    await callback.message.answer(f"Изменено состояние паузы у {serial_number}")
    await change_pause_db(serial_number=serial_number)

# Обработка нажатия кнопки "Изменить юзернейм"
@admin_search.callback_query(F.data.startswith("username_"))
async def change_username(callback: types.CallbackQuery, state: FSMContext):
    serial_number = callback.data.split("_")[-1]
    await callback.message.answer(f"Введите новый юзернейм для устройства с серийным номером {serial_number}:")
    await state.set_state(ChangeState.new_value)
    await state.update_data(serial_number=serial_number, field="username")


# Обработка нажатия кнопки "Изменить логин"
@admin_search.callback_query(F.data.startswith("login_"))
async def change_login(callback: types.CallbackQuery, state: FSMContext):
    serial_number = callback.data.split("_")[-1]
    await callback.message.answer(f"Введите новый логин для устройства с серийным номером {serial_number}:")
    await state.set_state(ChangeState.new_value)
    await state.update_data(serial_number=serial_number, field="login")


# Обработка нажатия кнопки "Изменить пароль"
@admin_search.callback_query(F.data.startswith("password_"))
async def change_password(callback: types.CallbackQuery, state: FSMContext):
    serial_number = callback.data.split("_")[-1]
    await callback.message.answer(f"Введите новый пароль для устройства с серийным номером {serial_number}:")
    await state.set_state(ChangeState.new_value)
    await state.update_data(serial_number=serial_number, field="password")


# Обработка нажатия кнопки "Изменить коментарий"
@admin_search.callback_query(F.data.startswith("comment_"))
async def change_comment(callback: types.CallbackQuery, state: FSMContext):
    serial_number = callback.data.split("_")[-1]
    await callback.message.answer(f"Введите новый коментарий для устройства с серийным номером {serial_number}:")
    await state.set_state(ChangeState.new_value)
    await state.update_data(serial_number=serial_number, field="comment")


# Обработка нового значения, отправленного пользователем
@admin_search.message(F.text, StateFilter(ChangeState.new_value))
async def process_new_value(message: types.Message, state: FSMContext):
    data = await state.get_data()
    serial_number = data.get("serial_number")
    field = data.get("field")
    new_value = message.text
    if field == "comment":
        await change_comment_db(serial_number=serial_number, new_comment=new_value)
    if field == "password":
        await change_password_db(serial_number=serial_number, new_password=new_value)
    if field == "login":
        await change_login_db(serial_number=serial_number, new_email=new_value)
    if field == "invoice":
        if new_value.isdigit():
            if int(new_value) > 31:
                await message.answer("Не такое большое")
                return
            today = datetime.datetime.today()
            invoice_day = datetime.datetime(
                year=today.year,
                month=today.month,
                day=int(new_value))
            if invoice_day < today:
                if today.month == 12:
                    invoice_day = datetime.datetime(
                        year=today.year + 1,
                        month=1,
                        day=int(new_value)
                    )
                else:
                    invoice_day = datetime.datetime(
                        year=today.year,
                        month=today.month + 1,
                        day=int(new_value)
                    )
            invoice_day.strftime("%Y-%m-%d")
        else:
            await message.answer("День должен быть числом")
            return
    if field == "username":
        await change_nickname(serial_number=serial_number, new_nickname=new_value)

    await state.clear()
    await message.answer("Изменения применены")
