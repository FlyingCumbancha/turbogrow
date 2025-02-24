import os
import yaml
from dotenv import load_dotenv

#  Detectar si estamos en Home Assistant o en entorno local
if os.path.exists("/config"):  # Home Assistant SIEMPRE tiene esta carpeta
    CONFIG_DIR = "/config/turbogrow"
else:
    CONFIG_DIR = os.path.dirname(__file__)

# Definir rutas de los archivos
ENV_FILE = os.path.join(CONFIG_DIR, ".env")
VARIABLES_FILE = os.path.join(CONFIG_DIR, "config/variables.yaml")
DB_PATH = os.path.join(CONFIG_DIR, "tasks.db")
#  Cargar variables de entorno desde .env si existe
if os.path.exists(ENV_FILE):
    load_dotenv(ENV_FILE)

#  Cargar configuración desde variables.yaml si existe
if os.path.exists(VARIABLES_FILE):
    with open(VARIABLES_FILE, "r") as f:
        config = yaml.safe_load(f)
else:
    config = {}

#  Asignar variables desde YAML o entorno
BOT_TOKEN = os.getenv("BOT_TOKEN", config.get("bot", {}).get("token"))
HA_URL = os.getenv("HA_URL", config.get("ha", {}).get("url"))
HA_TOKEN = os.getenv("HA_TOKEN", config.get("ha", {}).get("token"))
DB_USER = os.getenv("DB_USER", config.get("database", {}).get("user"))
DB_PASSWORD = os.getenv("DB_PASSWORD", config.get("database", {}).get("password"))

#  Datos de usuarios y admin
ADMIN_ID = config.get("admin", {}).get("id", "")
ADMIN_NAME = config.get("admin", {}).get("name", "")
USERS = config.get("users", [])

#  Mensaje de depuración (opcional, eliminar en producción)
print(f"📌 Configuración cargada desde: {CONFIG_DIR}")
