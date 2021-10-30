from sql_viewer.database import Database
from sql_viewer.database.query import QueryResult
from sql_viewer.errors import Result
from sql_viewer.errors.decorators import monadic
from sql_viewer.utils import (
    parse_column_names,
    parse_query,
    parse_schema,
    parse_results,
)


class TableService:
    def __init__(self, database: Database):
        self.database = database

    @monadic
    def get_tables(self) -> Result[QueryResult]:
        query = self.database.query(
            "SELECT name FROM sqlite_master WHERE type = 'table' AND name NOT LIKE 'sqlite_%'"
        )

        results = query.execute()

        return results.json

    @monadic
    def get_table_schema(self, tablename: str) -> Result[QueryResult]:
        query = self.database.query("PRAGMA table_info(%s)" % tablename)
        results = query.execute()
        return results.json

    @monadic
    def get_table_entries(self, tablename: str) -> Result[QueryResult]:
        query = self.database.query("SELECT * FROM %s" % tablename)
        results = query.execute()

        return results

    def get_table_pages(self, _tablename: str):
        return 0

    @monadic
    def get_database_schema(self) -> Result[list]:
        tables = self.get_tables().flat()

        database_schema = []

        for table in tables:
            table_schema = self.get_table_schema(table["name"]).flat()
            data = {"name": table["name"], "schema": table_schema}
            database_schema.append(data)

        return database_schema

    @monadic
    def execute_query(self, database_query: str) -> Result[QueryResult]:
        query = self.database.query(database_query)
        results = query.execute()
        return results
