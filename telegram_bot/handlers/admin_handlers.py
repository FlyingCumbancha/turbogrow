from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
from utils.tasks_manager import get_available_tasks, delete_task

def add_task_command(update: Update, context: CallbackContext):
    admin_id = context.bot_data.get('admin_id')
    if update.effective_user.id != admin_id:
        update.message.reply_text("No tienes permiso para usar este comando.")
        return

    # Se espera el formato: /addtask nombre-descripcion-frecuencia
    try:
        data = " ".join(context.args)
        name, description, frequency_str = data.split("-")
        frequency = int(frequency_str.strip())
    except Exception as e:
        update.message.reply_text(
            "Formato incorrecto. Usa: /addtask nombre-descripcion-frecuencia (0 para una tarea única)"
        )
        return

def delete_task_command(update: Update, context: CallbackContext):
    admin_id = context.bot_data.get('admin_id')
    if update.effective_user.id != admin_id:
        update.message.reply_text("No tienes permiso para usar este comando.")
        return

    tasks = get_available_tasks()
    if not tasks:
        update.message.reply_text("No hay tareas disponibles para eliminar.")
        return

    keyboard = []
    for task in tasks:
        task_id, name, _, _, _, _, _ = task
        keyboard.append([InlineKeyboardButton(name, callback_data=f"delete_{task_id}")])

    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Selecciona una tarea para eliminar:", reply_markup=reply_markup)

def confirm_delete_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()

    task_id = int(query.data.split("_")[1])

    # Preguntar si realmente quiere eliminar la tarea
    keyboard = [
        [InlineKeyboardButton("Sí, eliminar", callback_data=f"confirm_delete_{task_id}")],
        [InlineKeyboardButton("Cancelar", callback_data="cancel_delete")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    query.edit_message_text(f"¿Estás seguro de que deseas eliminar esta tarea?", reply_markup=reply_markup)

def delete_task_confirmed(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()

    task_id = int(query.data.split("_")[2])
    delete_task(task_id)

    query.edit_message_text("Tarea eliminada correctamente.")

def cancel_delete(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    query.edit_message_text("Eliminación cancelada.")
