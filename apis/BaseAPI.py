from abc import abstractmethod

class BaseAPI:
    def __init__(self):
        pass
    
    @staticmethod
    @abstractmethod
    def api_check_connection() -> (int, str):
        # This method should be implemented in the child class
        pass