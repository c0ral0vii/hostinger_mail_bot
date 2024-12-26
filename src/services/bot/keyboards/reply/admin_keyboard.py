from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def create_admin_keyboard():
    add_to_db = KeyboardButton(text="Добавить в базу")
    export_db = KeyboardButton(text="Выгрузить базу")
    change_everyday_message = KeyboardButton(text="Изменить сообщение дня")
    add_to_db_bot = KeyboardButton(text="Добавить в базу(бот)")
    find_in_db = KeyboardButton(text="Найти в базе(админ)")
    change_emails_button = KeyboardButton(text="Изменить почты")
    export_email = KeyboardButton(text="Выгрузить почты")
    admins = KeyboardButton(text="Админы")

    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [add_to_db, export_db],
            [change_everyday_message, add_to_db_bot],
            [find_in_db, admins],
            [change_emails_button, export_email]
        ],
        resize_keyboard=True,
    )

    return keyboard


def admins_keyboard():
    admin_delete = KeyboardButton(text="Удалить админа")
    add_admin = KeyboardButton(text="Добавить админа")
    all_admins = KeyboardButton(text="Получить админов")
    back = KeyboardButton(text="Назад")

    kb = ReplyKeyboardMarkup(
        keyboard=[
            [admin_delete, add_admin],
            [all_admins],
            [back],
        ],
        resize_keyboard=True,
    )

    return kb