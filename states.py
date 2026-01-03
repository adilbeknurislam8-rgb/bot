from aiogram.fsm.state import State, StatesGroup

class TaskState(StatesGroup):
    waiting_for_text = State()
    waiting_for_deadline = State()
