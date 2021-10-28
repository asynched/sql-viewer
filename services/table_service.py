from database import Database
from utils import parse_schema, parse_results


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
