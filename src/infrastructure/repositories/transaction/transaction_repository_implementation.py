from uuid import UUID
from domain.repositories.transaction.transaction_repository import TransactionRepository
from sqlalchemy.ext.asyncio import AsyncSession
from infrastructure.database.models.transaction import TransactionModel, TransactionCategoryEnum, TransactionStatusEnum
from sqlalchemy import select

class TransactionRepositoryImplementation(TransactionRepository):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_transaction(self, participant_id: str | UUID, amount: int, title: str, category: str = "TIKET") -> dict:
        try:
            transaction = TransactionModel(
                participant_id=participant_id,
                title=title,
                amount=amount,
                category=TransactionCategoryEnum.TIKET if category == "TIKET" else TransactionCategoryEnum.TOP_UP,
                status=TransactionStatusEnum.BERHASIL
            )

            self.db.add(transaction)
            await self.db.commit()
            await self.db.refresh(transaction)
            
            return transaction.to_dict()

        except ValueError as e:
            await self.db.rollback()
            raise e
        except Exception as e:
            await self.db.rollback()
            raise e

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
        
    async def get_transactions_by_participant_id(self, participant_id: str) -> dict:
        try:
            query = select(TransactionModel).where(TransactionModel.participant_id == participant_id).order_by(TransactionModel.created_at.desc())
            result = await self.db.execute(query)
            transactions = result.scalars().all()

            if transactions is None:
                return []

            return [transaction.to_dict() for transaction in transactions]

        except ValueError as e:
            raise e
        except Exception as e:
            raise e
