from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext

from src.services.bot.keyboards.reply.keyboards import create_start_keyboard

router = Router()


@router.message(F.text == "В главное меню")
async def to_main_menu(message: types.Message, state: FSMContext):
    await message.answer("Вы в главном меню", reply_markup=create_start_keyboard())