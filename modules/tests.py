import os

from .constants import paths
from .loggers import console
from .trend_vision_one import TrendVisionOne
from .errors import NetworkError, FileSystemError

def _network_test():
    try:
        console.debug("Comprobando conexión con Trend Vision One...")
        status_code, message = TrendVisionOne.checkAPIStatus()
        
        if status_code == 401:
            raise NetworkError(
                "[URGENTE]!!! El token de Trend Vision One ha expirado o no es válido.\n"
                "Por favor, actualice el token en el archivo de configuración. (.env)\n"
                "\n"
                "No se ha podido iniciar sesión en el servidor de Trend Vision One.\n"
                "Por favor, compruebe que el token es correcto.\n"
                "\n"
                "DETALLES:\n"
                f"{message}"
            )
        elif status_code != 200:
            print(message)
        else:
            console.debug("Conexión con Trend Vision One establecida.")
            return True
    except NetworkError as e:
        raise e
    except Exception as e:
        raise NetworkError("No se ha podido establecer conexión con Trend Vision One.\nPor favor, compruebe su conexión a Internet.")
    
    return False

def _paths_test():
    try:
        console.debug("Comprobando directorios necesarios para el funcionamiento de Trend Vision One...")
        
        for key, value in paths.items():
            if not os.path.exists(value):
                raise FileSystemError(f"El directorio {key} no existe.")
            if not os.path.isdir(value):
                raise FileSystemError(f"El directorio {key} no es un directorio.")
            if not os.access(value, os.W_OK):
                raise FileSystemError(f"El directorio {key} no tiene permisos de escritura.")
    except FileSystemError as e:
        raise e
    except Exception as e:
        raise FileSystemError("No se han podido crear los directorios necesarios para el funcionamiento de Trend Vision One.")
    
    return True

def test():
    try:
        _network_test()
        _paths_test()
        return True
    except NetworkError as e:
        console.error(f"NetworkError in test function: {e.message}")
        e.report()
    except FileSystemError as e:
        console.error(f"FileSystemError in test function: {e.message}")
    except Exception as e:
        console.error(e.message)
    
    return False
