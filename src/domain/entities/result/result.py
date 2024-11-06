from typing import Generic, TypeVar

T = TypeVar('T')

class Result(Generic[T]):
    def is_success(self) -> bool:
        return isinstance(self, Success)

    def is_failed(self) -> bool:
        return isinstance(self, Failed)

    def result_value(self):
        if self.is_success():
            return self.value
        return None

    def error_message(self):
        if self.is_failed():
            return self.message
        return None

class Success(Result[T]):
    def __init__(self, value: T):
        self.value = value

class Failed(Result[T]):
    def __init__(self, message: str):
        self.message = message