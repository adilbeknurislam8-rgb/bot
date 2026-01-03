import sqlite3

conn = sqlite3.connect("family.db")
cursor = conn.cursor()

# Таблица пользователей
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    name TEXT,
    role TEXT
)
""")

# Таблица задач
cursor.execute("""
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    text TEXT,
    deadline TEXT,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
)
""")

# Таблица целей
cursor.execute("""
CREATE TABLE IF NOT EXISTS goals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    text TEXT,
    deadline TEXT,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
)
""")

conn.commit()


# ===== Функции для работы с пользователями =====
def add_user(user_id, name, role="child"):
    cursor.execute(
        "INSERT OR IGNORE INTO users (user_id, name, role) VALUES (?, ?, ?)",
        (user_id, name, role)
    )
    conn.commit()


# ===== Функции для работы с задачами =====
def add_task(user_id, text, deadline):
    cursor.execute(
        "INSERT INTO tasks (user_id, text, deadline) VALUES (?, ?, ?)",
        (user_id, text, deadline)
    )
    conn.commit()


def get_tasks():
    rows = cursor.execute("""
        SELECT users.name, tasks.text, tasks.deadline
        FROM tasks JOIN users ON tasks.user_id = users.user_id
        ORDER BY tasks.id ASC
    """).fetchall()
    return [{"user": r[0], "text": r[1], "deadline": r[2]} for r in rows]


# ===== Функции для работы с целями =====
def add_goal(user_id, text, deadline):
    cursor.execute(
        "INSERT INTO goals (user_id, text, deadline) VALUES (?, ?, ?)",
        (user_id, text, deadline)
    )
    conn.commit()


def get_goals():
    rows = cursor.execute("""
        SELECT users.name, goals.text, goals.deadline
        FROM goals JOIN users ON goals.user_id = users.user_id
        ORDER BY goals.id ASC
    """).fetchall()
    return [{"user": r[0], "text": r[1], "deadline": r[2]} for r in rows]
