import time
from abc import ABC, abstractmethod
from sqlite3 import Cursor, Connection


class AbstractQuery(ABC):
    def __init__(self, query: str, args: tuple, cursor: Cursor, connection: Connection):
        self.query = query
        self.args = args
        self.cursor = cursor
        self.connection = connection

    @abstractmethod
    def execute(self):
        pass


class RawQuery(AbstractQuery):
    def execute(self):
        with self.connection:
            start = time.perf_counter()
            results = self.cursor.execute(self.query, self.args).fetchall()
            end = time.perf_counter()
            description = self.cursor.description

            return RawQueryResult(
                self.query, self.args, results, description, end - start
            )


class Query(AbstractQuery):
    def __init__(self, query: str, args: tuple, cursor: Cursor, connection: Connection):
        self.query = query
        self.args = args
        self.cursor = cursor
        self.connection = connection

    def execute(self):
        with self.connection:
            start = time.perf_counter()
            raw_results = self.cursor.execute(self.query, self.args).fetchall()
            end = time.perf_counter()

            columns = [column for (column, *_) in self.cursor.description]
            results = [list(item) for item in raw_results]

            return QueryResult(columns, results, len(results), end - start)


class QueryResult:
    def __init__(self, schema: list, results: list, items: int, time: float):
        self.schema = schema
        self.results = results
        self.items = items
        self.time = time

    def __str__(self):
        return (
            f"QueryResult<schema={self.schema}, items={self.items}, time={self.time}>"
        )

    @property
    def json(self):
        data = []

        for result in self.results:
            parsed = {}

            for index, key in enumerate(self.schema):
                parsed[key] = result[index]

            data.append(parsed)

        return data

    @property
    def full_json(self):
        return {
            "data": self.json,
            "time": self.time,
            "items": self.items,
        }


class RawQueryResult:
    def __init__(
        self, query: str, args: tuple, results: list, description: list, time: float
    ):
        self.query = query
        self.args = args
        self.results = results
        self.description = [column for (column, *_) in description]
        self.time = time

    def __str__(self):
        return f"RawQuery<query='{self.query}', args={self.args}, time={self.time}, description={self.description}, results='...'>"
