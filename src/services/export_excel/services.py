import pathlib
from openpyxl import Workbook
from src.services.database.orm.export import get_all_data
from typing import Dict, Any


async def create_export_file(data: Dict[str, Any] = get_all_data()) -> pathlib.Path:
    data = await get_all_data()

    workbook = Workbook()
    sheet = workbook.active
    sheet.title = 'export_data'

    headers = [
        "id", 'serial number', 'activated date', 'pay_day', 'pre-pay day', 'on pause',
        'phone', 'telegram username', 'username', 'email', 'password', 'pay_list'
    ]
    sheet.append(headers)

    for user_id, user_data in data.items():
        row = [
            user_id,
            user_data["serial_number"],
            user_data["activated_date"].strftime("%m/%d/%Y"),
            user_data["pay_day"].strftime("%m/%d/%Y"),
            user_data["pre_pay_day"].strftime("%m/%d/%Y"),
            '+' if user_data["on_pause"] else '-',
            user_data["phone"],
            user_data["tg_username"],
            user_data["username"],
            user_data["email"],
            user_data["password"],
            user_data["pay_list"]
        ]
        sheet.append(row)

    file_path = pathlib.Path().resolve() / 'temp' / 'export' / 'export_data.xlsx'
    workbook.save(file_path)

    return file_path