from sql_viewer.database import Database
from sql_viewer.database.query import QueryResult
from sql_viewer.errors import Result
from sql_viewer.errors.decorators import monadic
from sql_viewer.utils.array import flat


class APIService:
    def __init__(self, database: Database):
        self.database = database

    @monadic
    def get_table_list(self) -> Result[QueryResult]:
        return self.database.query(
            "SELECT * FROM sqlite_master "
            "WHERE type = 'table' AND NOT name = 'sqlite_%'"
        ).execute()

    @monadic
    def get_table(self, tablename: str) -> Result[QueryResult]:
        return self.database.query("SELECT * FROM %s" % tablename).execute()

    @monadic
    def get_database_schema(self) -> Result[list]:
        tablenames_result = self.database.query(
            "SELECT name FROM sqlite_master "
            "WHERE type = 'table' AND NOT name LIKE 'sqlite_%'"
        ).execute()

        tablenames = flat(tablenames_result.results)

        schemas = []

        for tablename in tablenames:
            result = self.database.query("PRAGMA table_info(%s)" % tablename).execute()

            schemas.append(
                {
                    "name": tablename,
                    "schema": result.json,
                }
            )

        return schemas

    @monadic
    def get_table_schema(self, tablename: str) -> Result[QueryResult]:
        return self.database.query("PRAGMA table_info(%s)" % tablename).execute()
