from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_code_kb(cross_number: str, user: bool = False):
    get_code = InlineKeyboardButton(text='Получить код', callback_data=f'get_code_{cross_number}')
    if not user:
        settings = InlineKeyboardButton(text="Изменить", callback_data=f'settings_{cross_number}')

        return  InlineKeyboardMarkup(inline_keyboard=[
            [get_code],
            [settings],
        ])

    else:
        return InlineKeyboardMarkup(inline_keyboard=[
            [get_code],
        ])