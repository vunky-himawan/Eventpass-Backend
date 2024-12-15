from domain.repositories.participant.participant_repository import ParticipantRepository
from sqlalchemy.ext.asyncio import AsyncSession
import uuid
from infrastructure.database.models.participant import ParticipantModel
from domain.entities.participant.participant import Participant
from infrastructure.database.models.user import UserModel
from sqlalchemy import select
from sqlalchemy.orm import selectinload

class ParticipantRepositoryImplementation(ParticipantRepository):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_participant_by_participant_id(self, participant_id: str | uuid.UUID) -> dict:
        try:
            query = select(ParticipantModel).where(ParticipantModel.participant_id == participant_id)
            result = await self.db.execute(query)
            participant = result.scalars().first()

            return participant.to_dict()

        except Exception as e:
            print(f"Error fetching participant: {e}")
            raise e
        
    async def get_participant_by_user_id(self, user_id: str | uuid.UUID) -> Participant:
        try:
            query = select(ParticipantModel).where(ParticipantModel.user_id == user_id)
            result = await self.db.execute(query)
            participant = result.scalars().first()

            participant = Participant(
                participant_name=participant.participant_name,
                participant_id=participant.participant_id,
                age=participant.age,
                gender=participant.gender,
                amount=participant.amount,
                created_at=participant.created_at,
                updated_at=participant.updated_at,
                birth_date=participant.birth_date
            )

            return participant

        except Exception as e:
            print(f"Error fetching participant: {e}")
            raise e
        
    async def get_participant_by_username(self, username: str) -> dict:
        try:
            query = select(ParticipantModel).options(selectinload(ParticipantModel.user)).where(UserModel.username == username)

            result = await self.db.execute(query)

            participant = result.scalars().first()

            return participant.participant_with_email()
            
        except Exception as e:
            print(f"Error fetching participant: {e}")
            raise e 
        
    async def subtract_balance(self, participant_id: str | uuid.UUID, amount: int) -> bool:
        try:
            participant = await self.db.get(ParticipantModel, participant_id)
            if not participant:
                return False
            
            participant.amount -= amount
            await self.db.commit()
            await self.db.refresh(participant)
            
            return True

        except Exception as e:
            print(f"Error subtracting balance: {e}")
            raise e

    async def add_balance(self, participant_id: str | uuid.UUID, amount: int) -> bool:
        try:
            participant = await self.db.get(ParticipantModel, participant_id)
            if not participant:
                return False
            
            participant.amount += amount
            await self.db.commit()
            await self.db.refresh(participant)
            
            return True

        except ValueError as e:
            await self.db.rollback()
            raise e
        except Exception as e:
            await self.db.rollback()
            raise e