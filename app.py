#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

# Check if Python version is 3.7 or higher
if not sys.version_info >= (3, 7):
    print("LogRhythm Intruder requiere Python 3.7 o superior.")
    sys.exit(1)

# Import modules
from modules.errors import TokenExpiredError, TokenNotSetError

from apis.Intruder import Intruder
from modules.setup import is_first_start, setup
from modules.cleanup import cleanup

from modules.utils import get_token_days
from modules.constants import config
from modules.loggers import console
from modules.tests import test

# Function to bootstrap the application
def bootstrap():
    # Check if token is set else raise error
    if not config["api"]["token"] or config["api"]["token"] == "":
        raise TokenNotSetError()
    
    # Check if token has expired
    if config["api"]["expiration"] and config["api"]["expiration"] != "":
        # Get expiration date in days return 0 if is invalid or expired
        expiration: int = get_token_days(config["api"]["expiration"])

        # If expiration date is less than current date, the token has expired
        if expiration <= 0:
            console.error("El token API ha expirado.")
            raise TokenExpiredError()
        
        # If expiration date is less than current date + 7 days, the token will expire soon
        elif expiration <= 7 and expiration > 0: 
            console.warn("Por favor, actualice el token en el archivo de configuración. (.env)\n"
            "Para obtener su token, vaya al siguiente enlace: https://developers.intruder.io/docs/authentication\n",
            "El token API expirará en menos de 7 días.")
    else:
        # If token is not set or is NULL raise warning
        console.warn("Advertencia: No se ha establecido una fecha de expiración para el token API.")
        console.warn("Si no establece una fecha de expiración, el sistema no podrá notificarle cuando el token expire.")
    
    # Check if is first start and setup
    if is_first_start():
        setup()

    # Test application before start, test token, folders, etc
    if not test(Intruder.api_check_connection):
        raise Exception("No se ha podido iniciar el programa. Los tests han fallado.")
    
    # Clean files that have already been read by LogRhythm
    cleanup()

    console.debug("El programa está listo para funcionar.")
    Intruder()

# Main function
if __name__ == "__main__":
    try:
        bootstrap()
    except Exception as e:
        console.error(e)
        sys.exit(1)
