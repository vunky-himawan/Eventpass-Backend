from domain.repositories.participant.participant_repository import ParticipantRepository
from sqlalchemy.ext.asyncio import AsyncSession
import uuid
from infrastructure.database.models.participant import ParticipantModel
from domain.entities.participant.participant import Participant
from sqlalchemy import select

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