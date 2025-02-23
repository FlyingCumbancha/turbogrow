def help_command(update, context):
    chat_id = update.effective_chat.id
    help_text = (
        "Comandos disponibles:\n"
        "/start - Iniciar el bot y recibir un mensaje de bienvenida.\n"
        "/help - Mostrar este mensaje de ayuda."
    )
    context.bot.send_message(chat_id=chat_id, text=help_text)
