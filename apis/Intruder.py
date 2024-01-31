import requests

from .BaseAPI import BaseAPI
from modules.constants import config
from modules.utils import get_ISO_8601


class Intruder(BaseAPI):
    def __init__(self):
        super().__init__()

    

    @staticmethod
    def api_check_connection():
        headers = {
            "Authorization": f"Bearer {config['api']['token']}",
        }

        r = requests.get("https://api.intruder.io/v1/health", headers=headers)

        if r.status_code == 401:
            return 401, "El token de acceso es inválido."
        elif r.status_code != 200:
            return r.status_code, "No se ha podido establecer conexión con el endpoint."
        return 200, "Conexión con el endpoint establecida."
