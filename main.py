import yaml
from telegram_bot.bot import iniciar_bot
from ha_integration.ha_client import conectar_ha
from utils.tasks_manager import init_db

def cargar_config():
    with open('config/config.yaml', 'r') as f:
        return yaml.safe_load(f)
    iniciar_bot(config)

def main():
    config = cargar_config()
    print("Configuración cargada:")
    print(config)
    
    # Probar la conexión con Home Assistant (stub)
    conectar_ha(config)
    
    # Iniciar el bot de Telegram
    iniciar_bot(config)

if __name__ == "__main__":
    # inicializar base de datos
    init_db()
    main()
