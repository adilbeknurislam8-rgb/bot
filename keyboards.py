from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def main_menu(role):
    buttons = [
        [InlineKeyboardButton(text="📝 Добавить задачу", callback_data="add_task")],
        [InlineKeyboardButton(text="📋 Задачи семьи", callback_data="all_tasks")]
    ]

    if role == "child":
        buttons = buttons[:1]

    return InlineKeyboardMarkup(inline_keyboard=buttons)
