def start_command(update, context):
    chat_id = update.effective_chat.id
    welcome_message = "¡Bienvenido a Crude Bot! Usa /help para ver los comandos disponibles."
    context.bot.send_message(chat_id=chat_id, text=welcome_message)
