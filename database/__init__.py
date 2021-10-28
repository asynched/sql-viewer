import sqlite3 as sql
from pathlib import Path
from config import DATABASE_FILENAME


class Database:
    ROOT_PATH = Path.cwd()

    def __init__(self):
        print(Database.ROOT_PATH)
        self.connection = sql.connect(
            Database.ROOT_PATH / DATABASE_FILENAME, check_same_thread=False
        )
        self.cursor = self.connection.cursor()
