from domain.repositories.event_participant.event_participant_repository import EventParticipantRepository
from sqlalchemy.ext.asyncio import AsyncSession
from infrastructure.database.models.event_participant import EventParticipantModel
from typing import List
from sqlalchemy import select
from infrastructure.database.models.event import EventModel
from datetime import datetime
from domain.entities.result.result import Result, Success, Failed


class EventParticipantRepositoryImplementation(EventParticipantRepository):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_event_participant(self, participant_id, event_id, ticket_id) -> bool:
        try:
            event_participant = EventParticipantModel(
                participant_id=participant_id,
                event_id=event_id,
                ticket_id=ticket_id
            )

            self.db.add(event_participant)
            await self.db.commit()
            await self.db.refresh(event_participant)
            
            return event_participant.to_dict()

        except ValueError as e:
            await self.db.rollback()
            raise e
        except Exception as e:
            await self.db.rollback()
            raise e
    
    async def get_events_participant_by_participant_id(self, participant_id):
        try:
            query = EventParticipantModel.query.filter(EventParticipantModel.participant_id == participant_id)
            result = await self.db.execute(query)
            event_participant = result.scalars().all()

            if event_participant is None:
                return []
            
            return [event_participant.to_dict() for event_participant in event_participant]

        except ValueError as e:
            print(f"Error fetching event participant: {e}")
            raise e
        except Exception as e:
            print(f"Error fetching event participant: {e}")
            raise e
        
    async def get_upcoming_participant_events(self, participant_id: str) -> List[dict]:
        try:
            query = select(EventParticipantModel).join(EventParticipantModel.event).where(EventParticipantModel.participant_id == participant_id).where(EventModel.start_date >= datetime.now())

            result = await self.db.execute(query)

            event_participants = result.scalars().all()

            if event_participants is None:
                return []
            
            return [event_participant.to_dict_with_event() for event_participant in event_participants]

        except ValueError as e:
            raise e
        except Exception as e:
            raise e
        
    async def check_is_purchased(self, event_id: str, participant_id: str) -> Result[dict]:
        try:
            query = select(EventParticipantModel).where(EventParticipantModel.event_id == event_id).where(EventParticipantModel.participant_id == participant_id)

            result = await self.db.execute(query)

            event_participant = result.scalar_one_or_none()

            if event_participant is None:
                return Failed(message="Event participant not found")
            
            return Success(value=event_participant.to_dict_with_relations())

        except ValueError as e:
            raise e
        except Exception as e:
            raise e