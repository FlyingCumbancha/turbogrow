from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
from utils.tasks_manager import get_available_tasks, delete_task, add_task
import logging
from config import ADMIN_ID

def is_admin(update: Update, context: CallbackContext) -> bool:
    """
    Verifica si el usuario que ejecuta el comando es el administrador.

    :param update: Objeto de actualización de Telegram
    :param context: Contexto del bot
    :return: True si el usuario es admin, False en caso contrario
    """
    user_id = update.effective_user.id

    logging.info(f"🔍 Comando intentado por: {user_id}, Admin registrado: {ADMIN_ID}")

    if not ADMIN_ID:
        update.message.reply_text("⚠️ Error: No se ha configurado el ADMIN_ID en el bot.")
        return False

    if str(user_id) != str(ADMIN_ID):  # Convertir ambos a string para evitar problemas de tipo
        update.message.reply_text("⛔ No tienes permiso para usar este comando.")
        return False

    return True

def add_task_command(update: Update, context: CallbackContext):
    """Permite al administrador agregar una nueva tarea."""
    if not is_admin(update, context):
        return

    try:
        data = " ".join(context.args).strip()
        if not data or data.count("-") != 2:
            raise ValueError("Formato incorrecto")

        name, description, frequency_str = map(str.strip, data.split("-"))

        if not name or not description or not frequency_str.isdigit():
            raise ValueError("Datos inválidos")

        frequency = int(frequency_str)

    except ValueError:
        update.message.reply_text(
            "❌ Formato incorrecto. Usa: /addtask nombre-descripcion-frecuencia (0 para una tarea única)."
        )
        return

    # Guardar la tarea en la base de datos
    add_task(name, description, frequency)
    
    logging.info(f"✅ Tarea agregada: {name} - {description} - Frecuencia: {frequency}")
    update.message.reply_text(f"✅ Tarea '{name}' agregada correctamente.")

def delete_task_command(update: Update, context: CallbackContext):
    """Muestra una lista de tareas para que el administrador elija cuál eliminar."""
    if not is_admin(update, context):
        return

    tasks = get_available_tasks()
    if not tasks:
        update.message.reply_text("ℹ️ No hay tareas disponibles para eliminar.")
        return

    keyboard = [[InlineKeyboardButton(name, callback_data=f"delete_{task_id}")] for task_id, name, *_ in tasks]
    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text("🗑️ Selecciona una tarea para eliminar:", reply_markup=reply_markup)

def confirm_delete_callback(update: Update, context: CallbackContext):
    """Pregunta al usuario si realmente desea eliminar una tarea."""
    query = update.callback_query
    query.answer()

    task_id = int(query.data.split("_")[1])

    keyboard = [
        [InlineKeyboardButton("✅ Sí, eliminar", callback_data=f"confirm_delete_{task_id}")],
        [InlineKeyboardButton("❌ Cancelar", callback_data="cancel_delete")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    query.edit_message_text(f"⚠️ ¿Estás seguro de que deseas eliminar esta tarea?", reply_markup=reply_markup)

def delete_task_confirmed(update: Update, context: CallbackContext):
    """Elimina una tarea tras la confirmación del usuario."""
    query = update.callback_query
    query.answer()

    task_id = int(query.data.split("_")[2])

    if delete_task(task_id):
        logging.info(f"🗑️ Tarea {task_id} eliminada correctamente.")
        query.edit_message_text("✅ Tarea eliminada correctamente.")
    else:
        logging.error(f"❌ Error al eliminar tarea {task_id}.")
        query.edit_message_text("❌ No se pudo eliminar la tarea.")

def cancel_delete(update: Update, context: CallbackContext):
    """Cancela la eliminación de una tarea."""
    query = update.callback_query
    query.answer()
    query.edit_message_text("❌ Eliminación cancelada.")
