# TurboManu

TurboManu es un bot de Telegram diseñado para la administración del "Crude de los Andes Cannabis Club". Este proyecto se integra como un add-on en Home Assistant, permitiendo gestionar dispositivos conectados de manera sencilla y centralizada. Además, cuenta con un sistema de administración que diferencia entre un usuario administrador y usuarios autorizados, y utiliza una base de datos para almacenar la información necesaria.

## Características

- **Integración con Home Assistant:** Controla y monitoriza dispositivos conectados a HA.
- **Administración de usuarios:** Soporta un usuario admin (definido en el archivo de configuración) y una lista de usuarios autorizados.
- **Interacción vía Telegram:** Incluye comandos básicos como /start y /help para iniciar y obtener asistencia.
- **Logging:** Registro de actividades a través de un archivo de configuración opcional (logging.conf).
- **Persistencia de datos:** Utiliza una base de datos para almacenar información relevante sobre el bot y sus interacciones.

## Estructura del Proyecto

La estructura del proyecto es la siguiente:

turbomanu/  
├── config/  
│   ├── config.yaml       # Contiene el token del bot, el ID del admin y la lista de usuarios autorizados (Telegram ID y nombre)  
│   └── logging.conf      # Configuración del logging (opcional)  
├── ha_integration/  
│   ├── ha_client.py      # Cliente para interactuar con la API de Home Assistant  
│   └── devices.py        # Funciones específicas para gestionar dispositivos conectados a HA  
├── telegram/  
│   ├── bot.py            # Inicialización y configuración del bot de Telegram  
│   ├── handlers/  
│   │   ├── admin_handlers.py  # Comandos y funciones especiales para el admin (usando el ID del config)  
│   │   └── user_handlers.py   # Comandos y funciones para usuarios autorizados (según la lista en config.yaml)  
│   └── commands/  
│       ├── start.py       # Lógica para el comando /start  
│       └── help.py        # Lógica para el comando /help y otros comandos básicos  
├── utils/  
│   ├── logger.py          # Utilidades para la gestión del logging  
│   └── helpers.py          # Funciones de ayuda generales  
├── main.py                # Punto de entrada de la aplicación, donde se inicializan los módulos y se conecta con HA  
├── requirements.txt       # Lista de dependencias y librerías necesarias  
└── README.md              # Documentación inicial del proyecto

## Configuración

1. **Archivo config.yaml:**  
   Define el token del bot, el ID del administrador y la lista de usuarios autorizados.  
   *Ejemplo:*

   telegram:
     token: "TU_TELEGRAM_BOT_TOKEN"
     admin_id: 123456789
     authorized_users:
       - id: 987654321
         name: "UsuarioEjemplo"

2. **Archivo logging.conf:**  
   Configura el logging para monitorear las actividades del bot y detectar errores.

## Instalación y Dependencias

1. **Clona el repositorio:**

   git clone https://github.com/flyingcumbancha/turbomanu.git  
   cd turbomanu

2. **Instala las dependencias:**

   pip install -r requirements.txt

3. **Configura el bot:**  
   Edita el archivo config/config.yaml con tus credenciales y demás datos necesarios.

## Ejecución

Para iniciar el bot, ejecuta el siguiente comando en la raíz del proyecto:

   python main.py

Esto inicializará la conexión con Home Assistant y activará el bot de Telegram para comenzar a recibir comandos.

## Integración con Home Assistant

El módulo ha_integration se encarga de gestionar la comunicación con Home Assistant a través de su API, permitiendo:
- Conectar y autenticar con HA.
- Enviar comandos y recibir información de los dispositivos conectados.

## Administración de Usuarios y Comandos

- **Admin:**  
  El archivo admin_handlers.py contiene comandos especiales que solo pueden ejecutar los administradores.

- **Usuarios autorizados:**  
  Los comandos básicos para usuarios se encuentran en user_handlers.py y en los scripts dentro de la carpeta commands (por ejemplo, /start y /help).

## Contribuciones

Si deseas contribuir a este proyecto:
- Realiza un fork del repositorio.
- Crea una rama para tus cambios.
- Envía un pull request con una descripción detallada de las modificaciones.

## Licencia

Este proyecto se distribuye bajo la licencia MIT. Consulta el archivo LICENSE para más detalles.

## Notas Finales

TurboManu es una herramienta en constante evolución. Se planea ampliar sus funcionalidades integrando nuevas características y mejoras tanto en la gestión de dispositivos de Home Assistant como en la experiencia de usuario en Telegram.

