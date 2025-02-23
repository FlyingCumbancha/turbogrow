from telegram import Update
from telegram.ext import CallbackContext
from utils.tasks_manager import add_task

def add_task_command(update: Update, context: CallbackContext):
    # Obtén el admin_id desde bot_data
    admin_id = context.bot_data.get('admin_id')
    if update.effective_user.id != admin_id:
        update.message.reply_text("No tienes permiso para usar este comando.")
        return

    # Se espera el formato: /addtask nombre|descripcion|frecuencia
    try:
        data = " ".join(context.args)
        name, description, frequency_str = data.split("|")
        frequency = int(frequency_str.strip())
    except Exception as e:
        update.message.reply_text(
            "Formato incorrecto. Usa: /addtask nombre|descripcion|frecuencia (0 para una tarea única)"
        )
        return

    add_task(name.strip(), description.strip(), frequency)
    update.message.reply_text("Tarea agregada correctamente.")
