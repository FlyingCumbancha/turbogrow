import logging

def setup_logger(name=__name__, level=logging.INFO):
    logger = logging.getLogger(name)
    if not logger.hasHandlers():
        logger.setLevel(level)
        # Configuración de un StreamHandler para imprimir en consola
        ch = logging.StreamHandler()
        ch.setLevel(level)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        logger.addHandler(ch)
    return logger

def get_logger(name=__name__, level=logging.INFO):
    return setup_logger(name, level)

# Logger global para uso en otros módulos
logger = setup_logger()
