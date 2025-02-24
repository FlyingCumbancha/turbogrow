import os
import yaml
from dotenv import load_dotenv

# Determinar si estamos en Home Assistant (Docker) o en local
RUNNING_IN_DOCKER = os.path.exists("/data/options.json")  # Presente solo en Home Assistant

if RUNNING_IN_DOCKER:
    CONFIG_DIR = "/root/config/turbomanu"  # Ruta en Home Assistant
else:
    CONFIG_DIR = os.path.join(os.getcwd(), "")  # Ruta local

# Definir rutas de los archivos
ENV_FILE = os.path.join(CONFIG_DIR, ".env")
VARIABLES_FILE = os.path.join(CONFIG_DIR, "config/variables.yaml")

# Cargar variables de entorno desde .env si existe
if os.path.exists(ENV_FILE):
    load_dotenv(ENV_FILE)

# Cargar configuración desde variables.yaml si existe
if os.path.exists(VARIABLES_FILE):
    with open(VARIABLES_FILE, "r") as f:
        config = yaml.safe_load(f)
else:
    config = {}

# Asignar variables desde YAML o entorno
BOT_TOKEN = os.getenv("BOT_TOKEN", config.get("bot", {}).get("token"))
HA_URL = os.getenv("HA_URL", config.get("ha", {}).get("url"))
HA_TOKEN = os.getenv("HA_TOKEN", config.get("ha", {}).get("token"))
DB_USER = os.getenv("DB_USER", config.get("database", {}).get("user"))
DB_PASSWORD = os.getenv("DB_PASSWORD", config.get("database", {}).get("password"))

# Datos de usuarios y admin
ADMIN_ID = config.get("admin", {}).get("id", "")
ADMIN_NAME = config.get("admin", {}).get("name", "")
USERS = config.get("users", [])
