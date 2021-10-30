from typing import TypeVar, Generic

T = TypeVar("T")


class Result(Generic[T]):
    def __init__(self, data: T, error: Exception):
        self.data = data
        self.error = error

    def flat(self) -> T:
        if self.error:
            raise self.error
        return self.data


class ResultError(TypeError):
    def __init__(self, message):
        super().__init__(message)
