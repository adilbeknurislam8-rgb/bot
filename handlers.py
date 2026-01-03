from aiogram import types, F, Router
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from pydantic import BaseModel
from database import add_user, add_task, get_tasks, add_goal, get_goals

# ===== Router =====
router = Router()

# ===== FSM States =====
class TaskGoalStates(StatesGroup):
    waiting_task_text = State()
    waiting_task_deadline = State()
    waiting_goal_text = State()
    waiting_goal_deadline = State()

# ===== Keyboard =====
main_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="📝 Добавить задачу"), 
            KeyboardButton(text="🎯 Добавить цель")
        ],
        [
            KeyboardButton(text="📋 Задачи семьи"), 
            KeyboardButton(text="🏆 Цели семьи")
        ]
    ],
    resize_keyboard=True
)

# ===== Pydantic Models =====
class TaskModel(BaseModel):
    user: str
    text: str
    deadline: str

class GoalModel(BaseModel):
    user: str
    text: str
    deadline: str

# ===== Handlers =====
@router.message(F.text == "/start")
async def start(message: types.Message, state: FSMContext):
    add_user(message.from_user.id, message.from_user.first_name)
    await message.answer("👋 Добро пожаловать в семейный планер!", reply_markup=main_kb)


@router.message()
async def main_menu(message: types.Message, state: FSMContext):
    if message.text == "📝 Добавить задачу":
        await message.answer("✍️ Напиши задачу")
        await state.set_state(TaskGoalStates.waiting_task_text)
    elif message.text == "🎯 Добавить цель":
        await message.answer("✍️ Напиши цель")
        await state.set_state(TaskGoalStates.waiting_goal_text)
    elif message.text == "📋 Задачи семьи":
        tasks = get_tasks()
        if not tasks:
            await message.answer("Список задач пуст.", reply_markup=main_kb)
            return
        text = "📋 Задачи семьи:\n"
        for t in tasks:
            text += f"👤 {t.user}\n📝 {t.text}\n⏰ {t.deadline}\n\n"
        await message.answer(text, reply_markup=main_kb)
    elif message.text == "🏆 Цели семьи":
        goals = get_goals()
        if not goals:
            await message.answer("Список целей пуст.", reply_markup=main_kb)
            return
        text = "🎯 Цели семьи:\n"
        for g in goals:
            text += f"👤 {g.user}\n📝 {g.text}\n⏰ {g.deadline}\n\n"
        await message.answer(text, reply_markup=main_kb)
    else:
        await message.answer("Выбери действие:", reply_markup=main_kb)


# ===== Add Task =====
@router.message(TaskGoalStates.waiting_task_text)
async def task_text(message: types.Message, state: FSMContext):
    await state.update_data(task_text=message.text)
    await message.answer("⏰ Введи дедлайн задачи (YYYY-MM-DD HH:MM)")
    await state.set_state(TaskGoalStates.waiting_task_deadline)

@router.message(TaskGoalStates.waiting_task_deadline)
async def task_deadline(message: types.Message, state: FSMContext):
    data = await state.get_data()
    add_task(message.from_user.id, data['task_text'], message.text)
    await message.answer("✅ Задача сохранена!", reply_markup=main_kb)
    await state.clear()

# ===== Add Goal =====
@router.message(TaskGoalStates.waiting_goal_text)
async def goal_text(message: types.Message, state: FSMContext):
    await state.update_data(goal_text=message.text)
    await message.answer("⏰ Введи дедлайн цели (YYYY-MM-DD)")
    await state.set_state(TaskGoalStates.waiting_goal_deadline)

@router.message(TaskGoalStates.waiting_goal_deadline)
async def goal_deadline(message: types.Message, state: FSMContext):
    data = await state.get_data()
    add_goal(message.from_user.id, data['goal_text'], message.text)
    await message.answer("✅ Цель сохранена!", reply_markup=main_kb)
    await state.clear()
