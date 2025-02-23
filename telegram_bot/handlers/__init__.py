from telegram.ext import CommandHandler
from telegram_bot.commands.start import start_command
from telegram_bot.commands.help import help_command

def registrar_handlers(dispatcher, config):
    # Registrar comando /start
    dispatcher.add_handler(CommandHandler("start", start_command))
    # Registrar comando /help
    dispatcher.add_handler(CommandHandler("help", help_command))
    
    print("Handlers registrados correctamente.")
