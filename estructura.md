crude_bot/
├── config/
│   ├── config.yaml         # Contendrá el token del bot, el ID del admin y la lista de usuarios autorizados (Telegram ID y nombre)
│   └── logging.conf        # Configuración del logging (opcional)
├── ha_integration/
│   ├── ha_client.py        # Cliente para interactuar con la API de Home Assistant
│   └── devices.py          # Funciones específicas para gestionar dispositivos conectados a HA
├── telegram/
│   ├── bot.py              # Inicialización y configuración del bot de Telegram
│   ├── handlers/
│   │   ├── admin_handlers.py   # Comandos y funciones especiales para el admin (usando el ID del config)
│   │   └── user_handlers.py    # Comandos y funciones para usuarios autorizados (según la lista en config.yaml)
│   └── commands/
│       ├── start.py        # Lógica para el comando /start
│       └── help.py         # Lógica para el comando /help y otros comandos básicos
├── utils/
│   ├── logger.py           # Utilidades para la gestión del logging
│   └── helpers.py          # Funciones de ayuda generales
├── main.py                 # Punto de entrada de la aplicación, donde se inicializan los módulos y se conecta con HA
├── requirements.txt        # Lista de dependencias y librerías necesarias
└── README.md               # Documentación inicial del proyecto
