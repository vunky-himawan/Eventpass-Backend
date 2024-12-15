from abc import ABC, abstractmethod
import uuid

class TransactionRepository(ABC):
    @abstractmethod
    async def create_transaction(self, participant_id: str | uuid.UUID, amount: int, title: str, category: str = "TIKET") -> dict:
        pass

    @abstractmethod
    async def get_transaction_by_transaction_id(self, transaction_id: str | uuid.UUID) -> dict:
        pass

    @abstractmethod
    async def get_transactions_by_participant_id(self, participant_id: str | uuid.UUID) -> dict:
        pass