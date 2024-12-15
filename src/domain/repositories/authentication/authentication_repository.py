from abc import ABC, abstractmethod
from domain.entities.user.user import User
from domain.entities.result.result import Result

class AuthenticationRepository(ABC):
    @abstractmethod
    async def get_user_by_username(self, username: str) -> Result[User]:
        pass

    @abstractmethod
    async def get_user_by_email(self, email: str) -> Result[User]:
        pass

    @abstractmethod
    async def get_logged_in_user(self, user_id: str) -> Result[User | None | dict]:
        pass