import datetime
import os.path

PROGRAMM = "CanSat"

DATA_DIR = "data"
LOG_DIR = os.path.join(DATA_DIR, "logs")
LOG_FILE = os.path.join(LOG_DIR, datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S.log'))


def get_conf_path(debug: bool = False) -> str:
    if debug:
        return os.path.join(DATA_DIR, "config.debug.yaml")
    return os.path.join(DATA_DIR, "config.yaml")
