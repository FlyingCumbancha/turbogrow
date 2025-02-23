from telegram.ext import Updater
from telegram_bot.handlers import registrar_handlers

def iniciar_bot(config):
    token = config['bot']['token']
    updater = Updater(token, use_context=True)
    registrar_handlers(updater.dispatcher, config)
    updater.start_polling()
    print("Bot iniciado y polling en marcha...")
    updater.idle()
