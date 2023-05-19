import datetime
import logging
from logging.handlers import RotatingFileHandler


def log():
    # fecha actual del registro
    now = datetime.datetime.now()
    #formato de la fecah que maneja los logs
    format_logger = now.strftime('%Y-%m-%d')
    #inicializacion de nuestro logger
    logger = logging.getLogger('')
    #seteo del nivel de logger, "recomendacion dejar en INFO para no ir registrando en nuestros los los debugs que pueden ser invasivos en el registro"
    logger.setLevel(logging.INFO)
    #manejador para la creacion de archivos
    handler = RotatingFileHandler(f'''logs/inventory-ms-{format_logger}.log''')
    formatter = logging.Formatter('%(asctime)s %(levelname)s | %(message)s')
    handler.setFormatter(formatter)

    if (logger.hasHandlers()):
        logger.handlers.clear()
    
    logger.addHandler(handler)

    return logger
