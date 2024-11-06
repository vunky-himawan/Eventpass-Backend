from abc import ABC, abstractmethod
from ...entities.user.user import User
from ...entities.result.result import Result


class AuthenticationRepository(ABC):
    @abstractmethod
    async def get_user_by_username(self, username: str) -> Result[User]:
        pass

    @abstractmethod
    async def get_user_by_email(self, email: str) -> Result[User]:
        pass

    @abstractmethod
    async def update_user_password(self, user_id: str, new_password: str, old_password: str) -> Result[bool]:
        pass