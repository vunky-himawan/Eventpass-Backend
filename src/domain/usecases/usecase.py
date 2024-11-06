from abc import ABC, abstractmethod
from typing import TypeVar, Generic

R = TypeVar('R')
P = TypeVar('P')

class Usecase(ABC, Generic[R, P]):
    @abstractmethod
    async def call(self, params: P) -> R:
        pass
