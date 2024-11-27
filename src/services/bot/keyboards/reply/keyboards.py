from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def create_start_keyboard():
    """Стартовая клавиатура"""

    find_in_base = KeyboardButton(text='Найти в базе')

    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [find_in_base],
        ],
        resize_keyboard=True
    )

    return keyboard