from utils.tasks_manager import get_available_tasks
from datetime import datetime, timedelta

def notify_due_tasks(context):
    tasks = get_available_tasks()
    now = datetime.now()
    for task in tasks:
        task_id, name, description, frequency, next_due, last_completed, responsible = task
        if next_due:
            # Parseamos la fecha usando el formato de almacenamiento
            next_due_dt = datetime.strptime(next_due, '%Y-%m-%d %H:%M')
            time_left = next_due_dt - now
            # Si quedan menos de 48 horas para que la tarea se deba realizar
            if time_left <= timedelta(hours=48):
                # Obtenemos la lista de usuarios registrados desde bot_data (se agregará en bot.py)
                users = context.bot_data.get('users', [])
                for user in users:
                    chat_id = user['id']
                    message = (
                        f"Recordatorio: La tarea <b>{name}</b> debe realizarse antes de "
                        f"{next_due_dt.strftime('%d-%m-%y %H:%M')}. Detalles: {description}"
                    )
                    context.bot.send_message(chat_id=chat_id, text=message, parse_mode="HTML")
