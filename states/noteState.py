from aiogram.fsm.state import State, StatesGroup

class Note(StatesGroup):
    body = State()