import os

from .constants import paths
from .loggers import console
from .errors import NetworkError, FileSystemError

def _network_test(check_connection_func: callable):
    try:
        console.debug("Comprobando conexión...")
        status_code, message = check_connection_func
        
        if status_code == 401:
            raise NetworkError("El token de acceso es inválido.")
        elif status_code != 200:
            print(message)
        else:
            console.debug("Conexión con el endpoint establecida.")
            return True
    except NetworkError as e:
        raise e
    except Exception as e:
        raise NetworkError("No se ha podido establecer conexión con el endpoint.\nPor favor, compruebe su conexión a Internet.")
    
    return False

def _paths_test():
    try:
        console.debug("Comprobando directorios...")
        
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
        raise FileSystemError("No se han podido crear los directorios necesarios para el funcionamiento del programa.")
    
    return True

def test(test_network: callable):
    try:
        _network_test(test_network)
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
