from typing import TypeVar, Generic

T = TypeVar("T")


class Result(Generic[T]):
    def __init__(self, data: T, error: Exception):
        self.data = data
        self.error = error
