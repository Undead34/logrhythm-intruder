from os import path
import os

from .constants import paths
from .loggers import console

def is_first_start():
    firstStart = False

    for key, value in paths.items():
        if not path.exists(value):
            firstStart = True
            break

    return firstStart

def setup():
    console.debug("Configurando Trend Vision One...")
    
    for key, value in paths.items():
        os.makedirs(value, exist_ok=True)
        console.debug(f"Directorio {key} creado en {value}")