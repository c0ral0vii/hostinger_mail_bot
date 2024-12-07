from aiogram.fsm.state import StatesGroup, State


class AddAdmin(StatesGroup):
    user_id = State()


class RemoveAdmin(StatesGroup):
    user_id = State()