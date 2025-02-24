from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
from telegram import BotCommand
from config import BOT_TOKEN  # Importamos directamente desde config.py
from telegram_bot.handlers import registrar_handlers
from telegram_bot.handlers.user_handlers import (
    list_tasks_command, task_detail_callback, complete_task_callback, return_to_start
)
from telegram_bot.handlers.admin_handlers import (
    add_task_command, delete_task_command, confirm_delete_callback, 
    delete_task_confirmed, cancel_delete
)
from telegram_bot.handlers.notifications import notify_due_tasks

def iniciar_bot(config):
    if not BOT_TOKEN:
        raise ValueError("❌ ERROR: El BOT_TOKEN no está configurado correctamente.")
    updater = Updater(BOT_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # Registra los handlers generales definidos en registrar_handlers
    registrar_handlers(dispatcher, config)

    # Registra los nuevos handlers para la gestión de tareas
    dispatcher.add_handler(CommandHandler("addtask", add_task_command))
    dispatcher.add_handler(CommandHandler("list_tasks", list_tasks_command))
    dispatcher.add_handler(CommandHandler("deltask", delete_task_command))
    dispatcher.add_handler(CallbackQueryHandler(task_detail_callback, pattern=r'^task_\d+'))
    dispatcher.add_handler(CallbackQueryHandler(complete_task_callback, pattern=r'^complete_\d+'))
    dispatcher.add_handler(CallbackQueryHandler(confirm_delete_callback, pattern=r'^delete_\d+'))
    dispatcher.add_handler(CallbackQueryHandler(delete_task_confirmed, pattern=r'^confirm_delete_\d+'))
    dispatcher.add_handler(CallbackQueryHandler(cancel_delete, pattern=r'^cancel_delete$'))
    dispatcher.add_handler(CallbackQueryHandler(return_to_start, pattern=r'^start$'))

    # Configura la lista de comandos que se mostrarán en el cliente de Telegram
    commands = [
        BotCommand("start", "Inicia el bot"),
        BotCommand("help", "Muestra ayuda"),
        BotCommand("list_tasks", "Lista las tareas disponibles"),
        BotCommand("addtask", "Agrega una tarea (solo admin)")
    ]

    updater.job_queue.run_repeating(notify_due_tasks, interval=3600, first=10)
    updater.bot.set_my_commands(commands)

    updater.start_polling()
    print("Bot iniciado y polling en marcha...")
    updater.idle()
