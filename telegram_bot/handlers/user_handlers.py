from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
from utils.tasks_manager import get_available_tasks, get_task_by_id, complete_task
from datetime import datetime

def list_tasks_command(update: Update, context: CallbackContext):
    tasks = get_available_tasks()
    if not tasks:
        update.message.reply_text("No hay tareas disponibles.")
        return

    keyboard = []
    for task in tasks:
        task_id, name, _, _, _, _, _ = task
        keyboard.append([InlineKeyboardButton(name, callback_data=f"task_{task_id}")])
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Selecciona una tarea:", reply_markup=reply_markup)

def task_detail_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    # Se espera callback data en el formato "task_{id}"
    task_id = int(query.data.split("_")[1])
    task = get_task_by_id(task_id)
    if not task:
        query.edit_message_text("Tarea no encontrada.")
        return

    task_id, name, description, frequency, next_due, last_completed, responsible = task

    # Modificar la cuenta regresiva para que se muestre como "Realizar tarea antes de: dd-mm-aa hh:mm"
    if next_due:
        next_due_dt = datetime.strptime(next_due, '%d-%m-%y %H:%M')
        formatted_next_due = next_due_dt.strftime('%d-%m-%y %H:%M')
        countdown_str = f"Realizar tarea antes de: {formatted_next_due}"
    else:
        countdown_str = "Realizar tarea antes de: N/A"

    text = (
        f"Nombre: {name}\n"
        f"Descripción: {description}\n"
        f"Frecuencia: {frequency} días\n"
        f"{countdown_str}\n"
        f"Última vez realizada: {last_completed if last_completed else 'Nunca'}\n"
        f"Ultimo en realizarla: {responsible if responsible else 'N/A'}"
    )

    keyboard = [
        [InlineKeyboardButton("Completar tarea", callback_data=f"complete_{task_id}")],
        [InlineKeyboardButton("Volver al inicio", callback_data="start")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(text, reply_markup=reply_markup)


def complete_task_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    # Se espera el callback data en el formato "complete_{id}"
    task_id = int(query.data.split("_")[1])
    user = update.effective_user
    complete_task(task_id, user.full_name)
    query.edit_message_text("Tarea completada. ¡Gracias!")
