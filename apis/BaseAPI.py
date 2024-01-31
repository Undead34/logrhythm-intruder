from abc import abstractmethod

class BaseAPI:
    def __init__(self, api_key, api_secret):
        self.api_key = api_key
        self.api_secret = api_secret


    @staticmethod
    @abstractmethod
    def api_check_connection() -> (int, str):
        # This method should be implemented in the child class
        pass