import yaml
from telegram_bot.bot import iniciar_bot
from ha_integration.ha_client import conectar_ha

def cargar_config():
    with open('config/config.yaml', 'r') as f:
        return yaml.safe_load(f)

def main():
    config = cargar_config()
    print("Configuración cargada:")
    print(config)
    
    # Probar la conexión con Home Assistant (stub)
    conectar_ha(config)
    
    # Iniciar el bot de Telegram
    iniciar_bot(config)

if __name__ == "__main__":
    main()
