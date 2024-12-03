from aiogram.fsm.state import StatesGroup, State


class InputNumberState(StatesGroup):
    number = State() # str


class FileState(StatesGroup):
    file = State()
    email_file = State()