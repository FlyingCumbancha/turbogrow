import sqlite3
from datetime import datetime, timedelta

DB_PATH = 'tasks.db'

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            frequency INTEGER,           -- 0: única vez; >0: días entre ejecuciones
            next_due TEXT,               -- Formato 'AAAA-MM-DD HH:MM'
            last_completed TEXT,
            responsible TEXT
        )
    ''')
    conn.commit()
    conn.close()

def add_task(name, description, frequency):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    # Si frequency > 0, se calcula el siguiente vencimiento; sino, queda en NULL
    if frequency > 0:
        next_due = (datetime.now() + timedelta(days=frequency)).strftime('%Y-%m-%d %H:%M')
    else:
        next_due = None
    c.execute(
        "INSERT INTO tasks (name, description, frequency, next_due) VALUES (?, ?, ?, ?)",
        (name, description, frequency, next_due)
    )
    conn.commit()
    conn.close()

def get_available_tasks():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    # Se muestran las tareas:
    # - Recurrencias (frequency > 0)
    # - Tareas únicas (frequency == 0) que aún no se han completado (last_completed IS NULL)
    c.execute("""
        SELECT id, name, description, frequency, next_due, last_completed, responsible 
        FROM tasks 
        WHERE (frequency > 0 OR (frequency = 0 AND last_completed IS NULL))
    """)
    tasks = c.fetchall()
    conn.close()
    return tasks

def get_task_by_id(task_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        SELECT id, name, description, frequency, next_due, last_completed, responsible 
        FROM tasks WHERE id = ?
    """, (task_id,))
    task = c.fetchone()
    conn.close()
    return task

def complete_task(task_id, user_name):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    now_str = datetime.now().strftime('%Y-%m-%d %H:%M')
    task = get_task_by_id(task_id)
    if not task:
        conn.close()
        return
    frequency = task[3]
    if frequency > 0:
        new_next_due = (datetime.now() + timedelta(days=frequency)).strftime('%Y-%m-%d %H:%M')
    else:
        new_next_due = None
    c.execute("""
        UPDATE tasks 
        SET last_completed = ?, responsible = ?, next_due = ?
        WHERE id = ?
    """, (now_str, user_name, new_next_due, task_id))
    conn.commit()
    conn.close()

def get_all_tasks():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM tasks")
    tasks = c.fetchall()
    conn.close()
    return tasks

def delete_task(task_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()
