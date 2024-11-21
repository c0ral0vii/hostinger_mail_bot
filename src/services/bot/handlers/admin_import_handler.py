from aiogram import Router, F, types
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

from logger.logger import setup_logger
from src.services.database.orm.import_excel import excel_import
from src.services.bot.filters.chat_type import ChatTypeFilter, IsAdmin
from src.services.bot.fsm.user_states import FileState
import pandas as pd


admin_import = Router(name='admin_import')
admin_import.message.filter(ChatTypeFilter(["private"]), IsAdmin())

logger = setup_logger(__name__)


@admin_import.message(F.text == 'Добавить в базу')
async def import_excel(message: types.Message, state: FSMContext):

    logger.info(f'Импорт @{message.from_user.username}')
    await message.answer('Отправьте файл .xlsx')

    await state.set_state(FileState.file)


@admin_import.message(F.document, StateFilter(FileState.file))
async def import_document(message: types.Message, state: FSMContext):
    document_id = message.document.file_id
    file = await message.bot.get_file(document_id)

    file_path = f"temp/input/{message.document.file_name}"
    await message.bot.download_file(file.file_path, file_path)

    try:
        await message.answer('База данных обновлена')
        df = pd.read_excel(file_path, header=0, engine='openpyxl')
        expected_columns = [
            "serial number",
            "activated date",
            "pay_day",
            "pre-pay day",
            "on pause",
            "phone",
            "telegram username",
            "username",
            "email",
            "password",
            "paylist"
        ]
        df.columns = expected_columns


        for index, row in df.iterrows():
            serial_number = row["serial number"]
            activated_date = row["activated date"]
            pay_day = row["pay_day"]
            pre_pay_day = row["pre-pay day"]
            on_pause = row["on pause"]
            phone = row["phone"]
            telegram_username = row["telegram username"]
            username = row["username"]
            email = row["email"]
            password = row["password"]
            paylist = row["paylist"]

            data = {
                'serial_number': str(serial_number),
                'activated_date': pd.to_datetime(activated_date),
                'pay_day': pd.to_datetime(pay_day),
                'pre_pay_day': pd.to_datetime(pre_pay_day),
                'on_pause': True if on_pause == '+' else False,
                'phone': str(phone).replace('+', '').replace('-', ''),
                'telegram_username': str(telegram_username),
                'username': str(username),
                'email': str(email),
                'password': str(password),
                'paylist': paylist,
            }

            await excel_import(data=data)

        await message.answer("База данных обновлена успешно!")
    except Exception as e:
        await message.answer(f"Ошибка при обработке файла: {e}")
