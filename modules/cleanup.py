import winreg
import os

from .errors import AgentError
from .constants import config
from .loggers import console

def cleanup():
    try:
        # X:\LogRhythm\LogRhythm System Monitor\state\[ID]
        state_path_RAW = f"{get_agent_state()}state\\" + config["log_source_id"]
        state_path = os.path.normpath(state_path_RAW)
        console.debug(f"Path to LogRhythm state: {state_path}")

        file_count = 0

        if not os.path.exists(state_path):
            console.error("No se ha encontrado el directorio de estado de LogRhythm.")
            return

        for file in os.listdir(state_path): # Iterate through all files in the directory
            if not file.endswith(".pos"):
                continue

            try:
                with open(os.path.join(state_path, file), "r") as f:  # Open the file
                    # Pos file example content:
                    # X:\path\to\vision_one.log
                    # 12478343
                    # 638408987240279906
                    pos_file = f.read().split("\n")  # pos_file = [path, number, number]
                    
                    if not os.path.exists(pos_file[0]):  # Check if the file exists
                        continue

                    # Check if the file size is equal to the size in the .pos file
                    if os.path.getsize(pos_file[0]) == int(pos_file[1]):  
                        os.remove(pos_file[0])
                        console.debug(f"Read of {pos_file[0]} complete.")
                        file_count += 1
            except Exception as e:
                console.error(f"Error al leer el archivo {file} Type: {type(e)}: {e}")

        console.debug(f"{file_count} files removed.")
    except AgentError as e:
        console.error(e.message)
    except Exception as e:
        console.error(f"Type: {type(e)}\n{e.message}")

# Getting Agent state location from registry.
def get_agent_state():
    try:
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\LogRhythm\scsm")
        agent_state, _ = winreg.QueryValueEx(key, "STATEPATH")
        return agent_state
    except FileNotFoundError:
        raise AgentError(
            "No se pudo encontrar la ubicación del estado del agente. "
            "Por favor, asegúrese de que el agente esté instalado."
        )
    except Exception as e:
        console.error(f"Type: {type(e)}\n{e.message}")
