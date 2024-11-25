from abc import ABC, abstractmethod
import uuid

class TransactionRepository(ABC):
    @abstractmethod
    async def get_transaction_by_transaction_id(self, transaction_id: str | uuid.UUID) -> dict:
        pass