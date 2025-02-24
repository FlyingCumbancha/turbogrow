import yaml
import os
from telegram_bot.bot import iniciar_bot
from ha_integration.ha_client import conectar_ha
from utils.tasks_manager import init_db
from config import BOT_TOKEN, HA_URL, HA_TOKEN, DB_USER, DB_PASSWORD  # ✅ Importamos variables directamente

def cargar_config():
    with open("config/config.yaml", "r") as f:
        config = yaml.safe_load(f)

    # Asegurar que las credenciales se tomen correctamente desde el entorno
    config["bot"]["token"] = BOT_TOKEN
    config["ha"]["url"] = HA_URL
    config["ha"]["token"] = HA_TOKEN
    config["database"]["user"] = DB_USER
    config["database"]["password"] = DB_PASSWORD

    return config

def main():
    config = cargar_config()
    print("✅ Configuración cargada correctamente:")
    print(config)
    
    # Probar la conexión con Home Assistant
    conectar_ha(config)

    # Iniciar el bot de Telegram sin pasar config si no es necesario
    iniciar_bot(config)  

if __name__ == "__main__":
    # Inicializar base de datos
    init_db()
    main()
