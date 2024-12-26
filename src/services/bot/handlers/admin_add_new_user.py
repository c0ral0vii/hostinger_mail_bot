import datetime

from aiogram import F, Router, types
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from src.services.bot.filters.chat_type import ChatTypeFilter, IsAdmin
from logger.logger import setup_logger
from src.services.database.orm.import_excel import excel_import

router = Router()
logger = setup_logger(__name__)
router.message.filter(ChatTypeFilter(["private"]), IsAdmin())


class AddNewUser(StatesGroup):
    serial_number = State()
    invoice_day = State()
    payment_day = State()
    activated_date = State()
    on_pause = State()
    phone = State()
    username = State()
    telegram_user = State()
    email = State()
    password = State()

    comment = State()
    final = State()


@router.message(F.text == "Добавить в базу(бот)")
async def admin_add_new_user(message: types.Message, state: FSMContext):
    await message.answer("Укажите серийный номер", reply_markup=InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Отмена", callback_data="cancel"),]
        ]
    ))
    await state.set_state(AddNewUser.serial_number)



@router.message(F.text, StateFilter(AddNewUser.serial_number))
async def admin_add_new_user(message: types.Message, state: FSMContext):
    await state.update_data(serial_number=message.text.upper())
    await message.answer("Укажите invoice day", reply_markup=InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Отмена", callback_data="cancel"),]
        ]
    ))

    await state.set_state(AddNewUser.invoice_day)


@router.message(F.text, StateFilter(AddNewUser.invoice_day))
async def admin_add_new_user(message: types.Message, state: FSMContext):
    await state.update_data(invoice_day=message.text)
    await message.answer("Укажите клиент на паузе или нет?(+ или -)", reply_markup=InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Отмена", callback_data="cancel"),]
        ]
    ))

    await state.set_state(AddNewUser.on_pause)


@router.message(F.text, StateFilter(AddNewUser.on_pause))
async def admin_add_new_user(message: types.Message, state: FSMContext):
    if message.text == "+":
        on_pause = True
    elif message.text == "-":
        on_pause = False
    else:
        await message.answer("Не правильное значение")
        return

    await state.update_data(on_pause=on_pause)
    await message.answer("Укажите номер мобильного телефона", reply_markup=InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Отмена", callback_data="cancel"),]
        ]
    ))

    await state.set_state(AddNewUser.phone)


@router.message(F.text, StateFilter(AddNewUser.phone))
async def admin_add_new_user(message: types.Message, state: FSMContext):
    await state.update_data(phone=message.text)
    await message.answer("Укажите юзернейм", reply_markup=InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Отмена", callback_data="cancel"), ]
        ]
    ))

    await state.set_state(AddNewUser.username)


@router.message(F.text, StateFilter(AddNewUser.username))
async def admin_add_new_user(message: types.Message, state: FSMContext):
    await state.update_data(username=message.text)
    await message.answer("Укажите telegram user", reply_markup=InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Отмена", callback_data="cancel"), ]
        ]
    ))

    await state.set_state(AddNewUser.telegram_user)


@router.message(F.text, StateFilter(AddNewUser.telegram_user))
async def admin_add_new_user(message: types.Message, state: FSMContext):
    await state.update_data(telegram_user=message.text)
    await message.answer("Укажите email", reply_markup=InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Отмена", callback_data="cancel"), ]
        ]
    ))

    await state.set_state(AddNewUser.email)

@router.message(F.text, StateFilter(AddNewUser.email))
async def admin_add_new_user(message: types.Message, state: FSMContext):
    await state.update_data(email=message.text)
    await message.answer("Укажите password", reply_markup=InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Отмена", callback_data="cancel"), ]
        ]
    ))

    await state.set_state(AddNewUser.password)


@router.message(F.text, StateFilter(AddNewUser.password))
async def admin_add_new_user(message: types.Message, state: FSMContext):
    await state.update_data(password=message.text)
    await message.answer("Укажите коментарий", reply_markup=InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Отмена", callback_data="cancel"), ]
        ]
    ))

    await state.set_state(AddNewUser.comment)


@router.message(F.text, StateFilter(AddNewUser.comment))
async def admin_add_new_user(message: types.Message, state: FSMContext):
    await state.update_data(comment=message.text)
    data = await state.get_data()
    logger.debug(data)
    data["invoice_day"] = int(data["invoice_day"])
    if data["invoice_day"] and isinstance(data["invoice_day"], int):
        today = datetime.datetime.today()
        invoice_day = datetime.datetime(
            year=today.year,
            month=today.month,
            day=data['invoice_day'])
        if invoice_day < today:
            if today.month == 12:
                invoice_day = datetime.datetime(
                    year=today.year + 1,
                    month=1,
                    day=data['invoice_day']
                )
            else:
                invoice_day = datetime.datetime(
                    year=today.year,
                    month=today.month + 1,
                    day=data['invoice_day']
                )
        invoice_day.strftime("%Y-%m-%d")
    else:
        invoice_day = None
    try:
        await excel_import(data={
            "serial_number": data["serial_number"],
            "on_pause": data["on_pause"],
            "pay_day": None,
            "activated_date": None,
            "invoice_day": invoice_day,
            "phone": data["phone"],
            "username": data["username"],
            "telegram_username": data["telegram_user"],
            "email": data["email"],
            "password": data["password"],
            "comment": data["comment"],
        })
        await message.answer('Успешно добавлено')
    except Exception as e:
        await message.answer(f'Произошла ошибка {e}')









