import sqlite3 as sql
from pathlib import Path
from sql_viewer.config import DATABASE_FILENAME
from sql_viewer.database.query import Query, RawQuery


class Database:
    ROOT_PATH = Path.cwd()

    def __init__(self):
        print(Database.ROOT_PATH)
        self.connection = sql.connect(
            Database.ROOT_PATH / DATABASE_FILENAME, check_same_thread=False
        )
        self.cursor = self.connection.cursor()

    def query(self, query: str, *args: tuple) -> Query:
        return Query(query, args, self.cursor, self.connection)

    def raw_query(self, query: str, *args: tuple):
        return RawQuery(query, args, self.cursor, self.connection)
