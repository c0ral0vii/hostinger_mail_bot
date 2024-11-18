from aiogram.fsm.state import StatesGroup, State


class InputNumberState(StatesGroup):
    number = State() # str