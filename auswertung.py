import os

DIR = "auswertung"
DB_FILE = "sqlite:///data.sql"


def setup():
    os.mkdir(DIR)
    os.removedirs(DIR)
    os.mkdir(DIR)


if __name__ == '__main__':
    setup()
