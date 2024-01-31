from .mailer import send_email
from .utils import get_ISO_8601

class NetworkError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

    def report(self):
        send_email(f"Event Date: {get_ISO_8601()}\n{self.message}")

class FileSystemError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class ConfigError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class AgentError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class TokenExpiredError(Exception):
    def __init__(self):
        self.message = (
            "Por favor, actualice el token en el archivo de configuración. (.env)\n"
            "Para obtener su token, vaya al siguiente enlace: https://automation.trendmicro.com/xdr/api-v3#tag/API-Keys\n"
            "El token de Trend Vision One ha expirado."
        )
        super().__init__(self.message)

class TokenNotSetError(Exception):
    def __init__(self):
        self.message = (
            "Por favor, establezca el token en el archivo de configuración. (.env)\n"
            "Para obtener su token, vaya al siguiente enlace: https://automation.trendmicro.com/xdr/api-v3#tag/API-Keys\n"
            "El token de Trend Vision One no está establecido."
        )
        super().__init__(self.message)