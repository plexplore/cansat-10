import datetime
import os.path

PROGRAMM = "CanSat"

DATA_DIR = "data"
LOG_DIR = os.path.join(DATA_DIR, "logs")
LOG_FILE = os.path.join(LOG_DIR, datetime.datetime.now().strftime('%Y-%m-%d-%H:%M:%S.log'))

args = {}
