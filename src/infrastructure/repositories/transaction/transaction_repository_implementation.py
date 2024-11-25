from uuid import UUID
from domain.repositories.transaction.transaction_repository import TransactionRepository
from sqlalchemy.ext.asyncio import AsyncSession
from infrastructure.database.models.transaction import TransactionModel
from sqlalchemy import select

class TransactionRepositoryImplementation(TransactionRepository):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_transaction_by_transaction_id(self, transaction_id: str | UUID) -> dict:
        try:
            query = select(TransactionModel).where(TransactionModel.transaction_id == transaction_id)
            result = await self.db.execute(query)
            transaction = result.scalars().first()

            if transaction is None:
                return None
            
            return transaction.to_dict()
        
        except ValueError as e:
            print(f"Error fetching transactions: {e}")
            raise e
        except Exception as e:
            print(f"Error fetching transactions: {e}")
            raise e