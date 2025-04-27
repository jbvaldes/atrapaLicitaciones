import logging
import os
from logging.handlers import RotatingFileHandler

# Configuración básica
def setup_logging():
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    # Formato del log
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    formatter = logging.Formatter(log_format)
    
    # Handler para archivo (rotativo)
    file_handler = RotatingFileHandler(
        f'{log_dir}/app.log',
        maxBytes=1024*1024,
        backupCount=5
    )
    file_handler.setFormatter(formatter)
    
    # Handler para consola
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    
    # Configurar logger raíz
    logging.basicConfig(
        level=logging.INFO,
        handlers=[file_handler, console_handler]
    )
