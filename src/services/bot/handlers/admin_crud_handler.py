import re
from aiogram import Router, F, Bot, types
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

from logger.logger import setup_logger
from src.services.bot.filters.chat_type import ChatTypeFilter, IsAdmin
from src.services.bot.fsm.admin_states import AddAdmin, RemoveAdmin
from src.services.bot.keyboards.reply.admin_keyboard import admins_keyboard, create_admin_keyboard
from src.services.database.orm.admins import (
    add_admin as add_admin_orm,
    delete_admin as delete_admin_orm,
    get_all_admins
)


admin_crud_router = Router(name="admin_crud_router")
admin_crud_router.message.filter(ChatTypeFilter(["private"]), IsAdmin())
pattern = r'[a-zA-Z]'

logger = setup_logger(__name__)


@admin_crud_router.message(F.text == "Админы")
async def admins(message: types.Message):
    await message.answer("Вы перешли во вкладку админов", reply_markup=admins_keyboard())


@admin_crud_router.message(F.text == "Назад")
async def back(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer("Вы были переброшены в главное меню", reply_markup=create_admin_keyboard())


@admin_crud_router.message(F.text == "Добавить админа")
async def add_admin(message: types.Message, state: FSMContext):
    await state.set_state(AddAdmin.user_id)
    await message.answer("Напишите юзер айди админа для добавления.\n\n@getmyid_bot - тут вы можете получить ваш айди")


@admin_crud_router.message(F.text, StateFilter(AddAdmin.user_id))
async def add_admin_state(message: types.Message, state: FSMContext):
    if re.search(pattern, message.text):
        await message.answer("Это не user_id!")
        return
    else:
        await state.update_data(user_id=int(message.text))
        data = await state.get_data()
        if isinstance(data['user_id'], int):
            await add_admin_orm({
                "user_id": data["user_id"],
            })

            await message.answer(f"Админ->{data['user_id']}\nДобавлен")
            await state.clear()
        else:
            await message.answer("Не правильно указан user_id, перепроверьте еще раз")

@admin_crud_router.message(F.text == "Удалить админа")
async def add_admin(message: types.Message, state: FSMContext):
    await state.set_state(RemoveAdmin.user_id)
    await message.answer("Напишите юзер айди админа для удаления.\n\n@getmyid_bot - тут вы можете получить ваш айди")


@admin_crud_router.message(F.text, StateFilter(RemoveAdmin.user_id))
async def delete_admin_state(message: types.Message, state: FSMContext):
    if re.search(pattern, message.text):
        await message.answer("Это не user_id!")
        return
    else:
        await state.update_data(user_id=int(message.text))
        data = await state.get_data()
        if isinstance(data['user_id'], int):
            await delete_admin_orm({
                "user_id": data["user_id"],
            })

            await message.answer(f"Админ->{data['user_id']}\nУдален")
            await state.clear()
        else:
            await message.answer("Не правильно указан user_id, перепроверьте еще раз")


@admin_crud_router.message(F.text == "Получить админов")
async def get_admins(message: types.Message, state: FSMContext):
    admins = await get_all_admins()
    await message.answer(f"Все ваши админы: \n{'\n'.join(f'{str(admin.user_id)}->{admin.username}' for admin in admins)}")