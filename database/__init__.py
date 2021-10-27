import sqlite3 as sql
from pathlib import Path


class Database:
    ROOT_PATH = Path.cwd()

    def __init__(self):
        print(Database.ROOT_PATH)
        self.connection = sql.connect(
            Database.ROOT_PATH / "northwind.sqlite3", check_same_thread=False
        )
        self.cursor = self.connection.cursor()
