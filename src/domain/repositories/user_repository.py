from abc import ABC, abstractmethod
from typing import List, Optional
from ..entities.user.user import User

class UserRepository(ABC):
    @abstractmethod
    async def get_by_id(self, id: int) -> Optional[User]:
        pass
    
    @abstractmethod
    async def get_all(self) -> List[User]:
        pass
    
    @abstractmethod
    async def create(self, user: User) -> User:
        pass