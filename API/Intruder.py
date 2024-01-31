from .BaseAPI import BaseAPI
from ..modules.utils import get_ISO_8601

class Intruder(BaseAPI):
    def __init__(self, api_key, api_secret):
        super().__init__(api_key, api_secret)