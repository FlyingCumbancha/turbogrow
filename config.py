import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
HA_URL = os.getenv("HA_URL")
HA_TOKEN = os.getenv("HA_TOKEN")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

# Validación para evitar valores vacíos
if not all([BOT_TOKEN, HA_URL, HA_TOKEN, DB_USER, DB_PASSWORD]):
    raise ValueError("❌ ERROR: Faltan variables de entorno en el archivo .env")

