from sql_viewer.database import Database
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

    def get_tables(self):
        query = """
            SELECT
                name
            FROM
                sqlite_master
            WHERE
                type = 'table' AND
                name NOT LIKE 'sqlite_%';
        """

        results = self.database.cursor.execute(query)

        parsed_results = [result for (result,) in results]

        return parsed_results

    def get_table_schema(self, tablename: str):
        query = (
            """
            PRAGMA table_info(%s);
            """
            % tablename
        )
        results = self.database.cursor.execute(query).fetchall()
        schema = parse_schema(results)
        return schema

    def get_table_entries(
        self,
        tablename: str,
        offset: int = 0,
        limit: int = 1000,
        schema: list = None,
    ):
        query = (
            """
            SELECT
                *
            FROM
                %s
            LIMIT
                ?, ?;
            """
            % tablename
        )

        if schema is None:
            schema = self.get_table_schema(tablename)

        results = self.database.cursor.execute(query, (offset, limit)).fetchall()
        entries = parse_results(results, schema)

        return entries

    def get_table_pages(self, tablename: str):
        query = (
            """
            SELECT
                COUNT(*)
            FROM
                %s;
            """
            % tablename
        )

        results = self.database.cursor.execute(query).fetchall()
        pages = results[0][0]

        return pages

    def get_database_schema(self):
        tables = self.get_tables()

        database_schema = []

        for table in tables:
            database_schema.append(
                {"table": table, "schema": self.get_table_schema(table)}
            )

        return database_schema

    def execute_query(self, query: str):
        results = self.database.cursor.execute(query).fetchall()
        column_names = parse_column_names(self.database.cursor.description)
        parsed_results = parse_query(results, column_names)
        schema = [{"column": column} for column in column_names]
        return [parsed_results, schema]

    @monadic
    def get_api_tables(self):
        query = self.database.query(
            "SELECT name, type, tbl_name FROM sqlite_master WHERE type = 'table' AND name NOT LIKE 'sqlite_%'"
        )

        return query.execute()
