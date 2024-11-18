from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def create_start_keyboard():
    """Стартовая клавиатура"""

    get_code = KeyboardButton(text='Получить код с почты')
    find_in_base = KeyboardButton(text='Найти в базе')

    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [get_code, find_in_base],
        ],
        resize_keyboard=True
    )

    return keyboard