from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def create_admin_keyboard():
    add_to_db = KeyboardButton(text="Добавить в базу")
    export_db = KeyboardButton(text="Выгрузить базу")
    find_in_db = KeyboardButton(text="Найти в базе(админ)")

    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [add_to_db, export_db],
            [find_in_db],
        ],
        resize_keyboard=True,
    )

    return keyboard