from dotenv import load_dotenv
import os

from .utils import sizeTextToNum

# If no .env file is found, create copy from .env.example
if not os.path.exists(".env"):
    print("No se ha encontrado el archivo .env. Creando copia de .env.example...")
    with open(".env.example", "r") as f:
        with open(".env", "w") as f2:
            f2.write(f.read())

# Load .env file and override if already exists
load_dotenv(override=True)

# Environment variables
config = {
    "api": {
        "token": os.environ.get("API_TOKEN", None),
        "expiration": os.environ.get("EXPIRATION_DATE_TOKEN", ""),
        "region": os.environ.get("REGION", "US"),
    },
    "smtp": {
        "email": os.environ.get("EMAIL", None),
        "password": os.environ.get("EMAIL_PASSWORD", None),
        "report_to": os.environ.get("EMAIL_REPORT", None),
    },
    "logger": {
        "max_size": sizeTextToNum(os.environ.get("MAX_FILE_SIZE", "8MB")),
        "max_files": int(os.environ.get("MAX_NUM_FILES", 50)),
    },
    "log_source_id": os.environ.get("LOG_SOURCE_ID", "0"),
    "oat": {
        "timedelta": int(os.environ.get("OAT_TIMEDELTA", 300)),
        "top": int(os.environ.get("OAT_TOP", 50)),
    },
}

base_path = os.path.realpath(os.path.join(os.path.curdir, "logs"))
paths = {
    "logs": base_path,
    "issues": os.path.join(base_path, "Issues"),
    "occurrences": os.path.join(base_path, "Occurrences"),
    "scanner_output": os.path.join(base_path, "Scanner Output"),
}
