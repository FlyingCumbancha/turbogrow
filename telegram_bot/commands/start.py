import logging
from telegram import Update, ParseMode
from telegram.ext import CallbackContext
from utils.logger import get_logger

logger = get_logger(__name__)

def start_command(update: Update, context: CallbackContext) -> None:
    """
    Función que maneja el comando /start.
    Muestra un mensaje de bienvenida personalizado e informativo.
    """
    user_first_name = update.effective_user.first_name if update.effective_user else "Cultivador"
    welcome_message = (
        f"🌱 *Bienvenido, {user_first_name}!* 🌱\n\n"
        "Soy *TurboManu*, el asistente de Cruce de los Andes Cannabis Club.\n\n"
        "Voy a gestionar las tareas del club para lograr ell cultivo ideal.\n\n"
        "Utiliza el comando /help para ver la lista de comandos disponibles.\n\n"
        "¡A DARLE ATOMOSSSS! 🚀"
    )
    
    # Enviar mensaje al usuario
    update.message.reply_text(welcome_message, parse_mode=ParseMode.MARKDOWN)
    logger.info(f"Comando /start ejecutado por {user_first_name}")

if __name__ == "__main__":
    # Modo prueba: simulación de llamada al comando /start
    from telegram import Update
    from telegram.ext import CallbackContext
    
    class DummyMessage:
        def reply_text(self, text, parse_mode=None):
            print(text)
    
    class DummyUser:
        first_name = "Tester"
    
    dummy_update = Update(update_id=0, message=type("Dummy", (), {"text": "/start", "reply_text": lambda self, msg, parse_mode=None: print(msg)})())
    dummy_update.effective_user = DummyUser()
    dummy_context = CallbackContext(None)
    start_command(dummy_update, dummy_context)
