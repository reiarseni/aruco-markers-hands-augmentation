"""
Módulo para configurar el sistema de logging a partir de un archivo de configuración YAML.
Este módulo permite definir múltiples handlers (consola, archivo, etc.) desde un archivo .yaml.
"""

import os
import logging
import yaml
from typing import Any, Dict, List

def configure_logging(config_path: str) -> None:
    """
    Configura el sistema de logging basado en la configuración especificada en un archivo YAML.

    Args:
        config_path (str): Ruta al archivo de configuración YAML.
    """
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"El archivo de configuración de logging no existe: {config_path}")

    with open(config_path, 'r', encoding='utf-8') as f:
        config: Dict[str, Any] = yaml.safe_load(f)

    # Limpiar los handlers existentes
    logger = logging.getLogger()
    logger.handlers = []

    # Establecer el nivel global de logging
    global_level_str: str = config.get('global_level', 'DEBUG')
    global_level = getattr(logging, global_level_str.upper(), logging.DEBUG)
    logger.setLevel(global_level)

    # Configurar cada handler definido en la configuración
    handlers: List[Dict[str, Any]] = config.get('handlers', [])
    for handler_conf in handlers:
        handler_type = handler_conf.get('type', 'console').lower()
        level_str = handler_conf.get('level', 'DEBUG')
        level = getattr(logging, level_str.upper(), logging.DEBUG)
        fmt = handler_conf.get('format', "%(asctime)s [%(levelname)s] %(message)s")
        formatter = logging.Formatter(fmt)

        if handler_type == 'console':
            handler = logging.StreamHandler()
        elif handler_type == 'file':
            filename = handler_conf.get('filename', 'app.log')
            mode = handler_conf.get('mode', 'a')
            # Asegurarse de que el directorio del archivo exista
            directory = os.path.dirname(filename)
            if directory and not os.path.exists(directory):
                os.makedirs(directory, exist_ok=True)
            handler = logging.FileHandler(filename, mode=mode)
        else:
            raise ValueError(f"Tipo de handler desconocido: {handler_type}")

        handler.setLevel(level)
        handler.setFormatter(formatter)
        logger.addHandler(handler)
