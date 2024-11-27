from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_code_kb(cross_number: str):
    get_code = InlineKeyboardButton(text='Получить код', callback_data=f'get_code_{cross_number}')

    return  InlineKeyboardMarkup(inline_keyboard=[
        [get_code],
    ])