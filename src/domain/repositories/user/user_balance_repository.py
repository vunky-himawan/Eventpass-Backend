from ....domain.repositories.user.user_repository import UserRepository
from abc import abstractmethod
from ....domain.entities.result.result import Result

class UserBalanceRepository(UserRepository):
    @abstractmethod
    async def get_user_balance(self, user_id: int) -> Result[int]:
        pass

    @abstractmethod
    async def update_user_balance(self, user_id: int, amount: int) -> Result[int]:
        pass