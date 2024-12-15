from domain.repositories.event_organizer.event_organizer_repository import EventOrganizerRepository
from sqlalchemy.ext.asyncio import AsyncSession
from domain.entities.result.result import Result, Failed, Success
from infrastructure.database.models.event_organizer import EventOrganizerModel
import uuid
from sqlalchemy.future import select

class EventOrganizerRepositoryImplementation(EventOrganizerRepository):
    def __init__(self, db: AsyncSession):
        self.db = db
        
    async def get_event_organizer_by_event_organizer_id(self, event_organizer_id) -> Result[dict]:
        try:
            query = select(EventOrganizerModel).where(EventOrganizerModel.event_organizer_id == event_organizer_id)
            event_organizer = await self.db.execute(query)
            event_organizer = event_organizer.scalar_one()

            if event_organizer is None:
                return Failed(message="Event organizer not found")
            
            return Success(value=event_organizer.to_dict())
        except ValueError as e:
            print(f"Error fetching event organizer: {e}")
            raise e
        except Exception as e:
            print(f"Error fetching event organizer: {e}")
            raise e
        
    
    async def subtract_balance(self, event_organizer_id: str | uuid.UUID, amount: int) -> bool:
        try:
            event_organizer = await self.db.get(EventOrganizerModel, event_organizer_id)
            if not event_organizer:
                return False
            
            event_organizer.amount -= amount
            await self.db.commit()
            await self.db.refresh(event_organizer)
            
            return True

        except ValueError as e:
            await self.db.rollback()
            raise e
        except Exception as e:
            await self.db.rollback()
            raise e

    async def add_balance(self, event_organizer_id: str | uuid.UUID, amount: int) -> bool:
        try:
            event_organizer = await self.db.get(EventOrganizerModel, event_organizer_id)
            if not event_organizer:
                return False
            
            event_organizer.amount += amount
            await self.db.commit()
            await self.db.refresh(event_organizer)
            
            return True

        except ValueError as e:
            await self.db.rollback()
            raise e
        except Exception as e:
            await self.db.rollback()
            raise e