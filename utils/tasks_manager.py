import sqlite3
from datetime import datetime, timedelta
from config import DB_PATH

def init_db():
    """Crea la tabla de tareas si no existe."""
    try:
        with sqlite3.connect(DB_PATH) as conn:
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
        print("✅ Base de datos inicializada correctamente.")
    except sqlite3.Error as e:
        print(f"❌ Error al inicializar la base de datos: {e}")

def add_task(name, description, frequency):
    """Agrega una nueva tarea a la base de datos."""
    try:
        next_due = (datetime.now() + timedelta(days=frequency)).strftime('%Y-%m-%d %H:%M') if frequency > 0 else None

        print(f"📝 Intentando agregar tarea: {name} - {description} - Frecuencia: {frequency}, Próximo vencimiento: {next_due}")

        with sqlite3.connect(DB_PATH) as conn:
            c = conn.cursor()
            c.execute(
                "INSERT INTO tasks (name, description, frequency, next_due) VALUES (?, ?, ?, ?)",
                (name, description, frequency, next_due)
            )
            conn.commit()

            # Verificar si la tarea realmente fue insertada
            c.execute("SELECT * FROM tasks ORDER BY id DESC LIMIT 1")
            last_task = c.fetchone()

        if last_task:
            print(f"✅ Tarea agregada en la base de datos: {last_task}")
        else:
            print("❌ ERROR: La tarea no fue agregada correctamente.")

    except sqlite3.Error as e:
        print(f"❌ Error al agregar tarea: {e}")


def get_available_tasks():
    """Obtiene todas las tareas pendientes o recurrentes."""
    try:
        with sqlite3.connect(DB_PATH) as conn:
            c = conn.cursor()
            c.execute("""
                SELECT id, name, description, frequency, next_due, last_completed, responsible 
                FROM tasks 
                WHERE (frequency > 0 OR (frequency = 0 AND last_completed IS NULL))
            """)
            tasks = c.fetchall()
        print(f"📋 {len(tasks)} tareas disponibles encontradas.")
        return tasks
    except sqlite3.Error as e:
        print(f"❌ Error al obtener tareas disponibles: {e}")
        return []

def get_task_by_id(task_id):
    """Obtiene una tarea por su ID."""
    try:
        with sqlite3.connect(DB_PATH) as conn:
            c = conn.cursor()
            c.execute("""
                SELECT id, name, description, frequency, next_due, last_completed, responsible 
                FROM tasks WHERE id = ?
            """, (task_id,))
            task = c.fetchone()
        if task:
            print(f"🔍 Tarea encontrada: {task}")
        else:
            print(f"⚠️ No se encontró tarea con ID {task_id}")
        return task
    except sqlite3.Error as e:
        print(f"❌ Error al obtener tarea: {e}")
        return None

def complete_task(task_id, user_name):
    """Marca una tarea como completada y actualiza su próximo vencimiento si es recurrente."""
    try:
        task = get_task_by_id(task_id)
        if not task:
            return False

        now_str = datetime.now().strftime('%Y-%m-%d %H:%M')
        frequency = task[3]
        new_next_due = (datetime.now() + timedelta(days=frequency)).strftime('%Y-%m-%d %H:%M') if frequency > 0 else None

        with sqlite3.connect(DB_PATH) as conn:
            c = conn.cursor()
            c.execute("""
                UPDATE tasks 
                SET last_completed = ?, responsible = ?, next_due = ?
                WHERE id = ?
            """, (now_str, user_name, new_next_due, task_id))
            conn.commit()
        
        print(f"✅ Tarea {task_id} completada por {user_name}.")
        return True
    except sqlite3.Error as e:
        print(f"❌ Error al completar tarea: {e}")
        return False

def get_all_tasks():
    """Obtiene todas las tareas de la base de datos."""
    try:
        with sqlite3.connect(DB_PATH) as conn:
            c = conn.cursor()
            c.execute("SELECT * FROM tasks")
            tasks = c.fetchall()
        print(f"📋 Total de tareas en la base de datos: {len(tasks)}")
        return tasks
    except sqlite3.Error as e:
        print(f"❌ Error al obtener todas las tareas: {e}")
        return []

def delete_task(task_id):
    """Elimina una tarea de la base de datos."""
    try:
        with sqlite3.connect(DB_PATH) as conn:
            c = conn.cursor()
            c.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
            conn.commit()
        print(f"🗑️ Tarea {task_id} eliminada correctamente.")
        return True
    except sqlite3.Error as e:
        print(f"❌ Error al eliminar tarea: {e}")
        return False

# Inicializar base de datos al cargar el módulo
init_db()
