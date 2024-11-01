from abc import ABC, abstractmethod
from typing import TypeVar, Generic

# Mendefinisikan TypeVar untuk generik
R = TypeVar('R')
P = TypeVar('P')

class Usecase(ABC, Generic[R, P]):
    @abstractmethod
    async def __call__(self, params: P) -> R:
        pass