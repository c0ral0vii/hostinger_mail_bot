from aiogram import Router, F, types
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from src.services.bot.filters.chat_type import ChatTypeFilter, IsAdmin
from src.services.database.orm.everyday_message import change_message, create_everyday_message

router = Router()
router.message.filter(ChatTypeFilter(["private"]), IsAdmin())

class EverydayState(StatesGroup):
    message = State()


@router.message(F.text == "Изменить сообщение дня")
async def change_everyday_message(message: types.Message, state: FSMContext):
    everyday_message = await create_everyday_message()

    await message.answer(f"Установленое сообщение: {everyday_message.message}\n\nОтправьте новое сообщение дня:", reply_markup=InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Отмена", callback_data="cancel")]
        ]
    ))
    await state.set_state(EverydayState.message)


@router.callback_query(F.data == "cancel")
async def cancel(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.answer("Состояние установки отменено")
    await state.clear()


@router.message(F.text, StateFilter(EverydayState))
async def new_everyday_message(message: types.Message, state: FSMContext):
    text = message.text

    new_message = await change_message(text=text)

    await message.answer(new_message["message"])

    await state.clear()
