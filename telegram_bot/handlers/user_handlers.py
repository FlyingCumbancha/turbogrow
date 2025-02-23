from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
from utils.tasks_manager import get_available_tasks, get_task_by_id, complete_task
from datetime import datetime

def list_tasks_command(update: Update, context: CallbackContext):
    tasks = get_available_tasks()
    if not tasks:
        update.message.reply_text("No hay tareas disponibles.")
        return

    message_lines = []
    keyboard = []
    for task in tasks:
        task_id, name, description, frequency, next_due, last_completed, responsible = task
        
        # Formatear la próxima fecha (next_due)
        if next_due:
            next_due_dt = datetime.strptime(next_due, '%Y-%m-%d %H:%M')
            formatted_next_due = next_due_dt.strftime('%d-%m-%y %H:%M')
        else:
            formatted_next_due = "N/A"
        
        # Agregar una línea al mensaje con el título y la próxima fecha
        message_lines.append(f"• {name} - Realizar antes de: {formatted_next_due}")
        
        # Agregar un botón para la tarea
        keyboard.append([InlineKeyboardButton(name, callback_data=f"task_{task_id}")])
    
    message_text = "Tareas disponibles:\n" + "\n".join(message_lines) + "\n\nSelecciona una tarea para ver más detalles."
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(message_text, reply_markup=reply_markup)

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
        next_due_dt = datetime.strptime(next_due, '%Y-%m-%d %H:%M')
        formatted_next_due = next_due_dt.strftime('%d-%m-%y %H:%M')
        countdown_str = f"Realizar tarea antes de: {formatted_next_due}"
    else:
        countdown_str = "Realizar tarea antes de: N/A"
    
    if last_completed:
        last_completed_dt = datetime.strptime(last_completed, '%Y-%m-%d %H:%M')
        formatted_last_completed = last_completed_dt.strftime('%d-%m-%y %H:%M')
    else:
        formatted_last_completed = "Nunca"

    text = (
        f"Nombre: {name}\n"
        f"Descripción: {description}\n"
        f"Frecuencia: {frequency} días\n"
        f"{countdown_str}\n"
        f"Última vez realizada: {formatted_last_completed if formatted_last_completed else 'Nunca'}\n"
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
