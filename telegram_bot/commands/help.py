import logging
from telegram import Update, ParseMode
from telegram.ext import CallbackContext
from utils.logger import get_logger

logger = get_logger(__name__)

def help_command(update: Update, context: CallbackContext) -> None:
    user_first_name = update.effective_user.first_name if update.effective_user else "Cultivador"
    """
    Función que maneja el comando /help.
    Muestra una guía de los comandos disponibles, centrada en el manejo de tareas.
    """
    help_message = (
        "📖 *Comandos Disponibles en TurboManu* 📖\n\n"
        "• */start* - Inicia el bot y muestra el mensaje de bienvenida.\n"
        "• */help* - Muestra esta ayuda detallada.\n"
        "• */list_tasks* - Lista todas las tareas pendientes.\n"
        "• */addtask* - Agrega una nueva tarea. Solo ADMIN\n"
        "• */deltask* - Elimina una tarea. Solo ADMIN \n\n"
    )
    
    update.message.reply_text(help_message, parse_mode=ParseMode.MARKDOWN)
    logger.info(f"Comando /help ejecutado por {user_first_name}")

if __name__ == "__main__":
    # Modo prueba: simulación de llamada al comando /help
    from telegram import Update
    from telegram.ext import CallbackContext
    
    class DummyMessage:
        def reply_text(self, text, parse_mode=None):
            print(text)
    
    class DummyUser:
        first_name = "Tester"
    
    dummy_update = Update(update_id=0, message=type("Dummy", (), {
        "text": "/help", 
        "reply_text": lambda self, msg, parse_mode=None: print(msg)
    })())
    dummy_update.effective_user = DummyUser()
    dummy_context = CallbackContext(None)
    help_command(dummy_update, dummy_context)
