import pathlib
from openpyxl import Workbook
from src.services.database.orm.export import get_all_data, get_all_data_emails
from typing import Dict, Any


async def create_export_file_users(data: Dict[str, Any] = get_all_data(), filename: str = 'export_data', to_temp = False) -> pathlib.Path:
    data = await get_all_data()

    workbook = Workbook()
    sheet = workbook.active
    sheet.title = 'export_data'

    headers = [
        'serial number', 'activated date', 'pay_day', 'invoice_day', 'on pause',
        'phone', 'telegram username', 'username', 'email', 'password', 'pay_list', 'comment'
    ]
    sheet.append(headers)

    for user_id, user_data in data.items():
        row = [
            user_data["serial_number"],
            "-" if user_data["activated_date"] is None else user_data["activated_date"].strftime("%d.%m.%Y"),
            "-" if user_data["pay_day"] is None else user_data["pay_day"].strftime("%d.%m.%Y"),
            "-" if user_data["invoice_day"] is None else user_data["invoice_day"].strftime("%d"),
            '+' if user_data["on_pause"] else '-',
            user_data["phone"],
            user_data["tg_username"],
            user_data["username"],
            user_data["email"],
            user_data["password"],
            user_data["pay_list"],
            user_data["comment"],
        ]
        sheet.append(row)

    file_path = pathlib.Path().resolve() / 'temp' / 'export' / f'{filename}.xlsx'

    if to_temp:
        file_path = pathlib.Path().resolve() / 'temp' / '_database_save' / f'{filename}.xlsx'

    workbook.save(file_path)

    return file_path


async def create_export_file_emails(data: Dict[str, Any] = get_all_data(), filename: str = 'export_email') -> pathlib.Path:
    data = await get_all_data_emails()

    workbook = Workbook()
    sheet = workbook.active
    sheet.title = 'export_email'

    headers = ["email", "password"]

    sheet.append(headers)

    for email_id, email_data in data.items():
        row = [
            email_data["email"],
            email_data["password"],
        ]
        sheet.append(row)

    file_path = pathlib.Path().resolve() / 'temp' / 'export' / f'{filename}.xlsx'
    workbook.save(file_path)

    return file_path
