from typing import Optional
import uuid
from infrastructure.database.models.event import EventModel
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import and_, or_
from domain.repositories.event.main import EventRepository

class EventRepositoryImplementation(EventRepository):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self):
        try:
            events = await self.db.execute(
                    select(EventModel)
                    .order_by(EventModel.created_at.desc())
            )
            return events.scalars().all()
        except Exception as e:
            print(f"Error fetching events: {e}")
            raise e

    async def get_event(self, event_id:str | uuid.UUID):
        try:
            events = await self.db.execute(
                    select(EventModel).where(EventModel.c.event_id == event_id)
            )

            if events.scalars().first() is None:
                return None;

            return events.scalars().first()
        except Exception as e:
            print(f"Error fetching events: {e}")
            raise e

    async def create_event(
            self,
            title: str,
            thumbnail_path: str, 
            event_organizer_id: str,
            address: str, 
            description: str, 
            type: str, 
            status: str, 
            ticket_price: int, 
            ticket_quantity: int, 
            start_date: str,
            receptionist_1: uuid.UUID,
            receptionist_2: Optional[uuid.UUID] = None,
        ):
        try:
            event = EventModel(
                    event_organizer_id=event_organizer_id,
                    title=title,
                    thumbnail_path=thumbnail_path,
                    address=address,
                    description=description,
                    type=type,
                    status=status,
                    ticket_price=ticket_price,
                    ticket_quantity=ticket_quantity,
                    start_date=start_date,
                    receptionist_1=receptionist_1,
                    receptionist_2=receptionist_2
            )
            self.db.add(event)
            await self.db.commit()
            await self.db.refresh(event)
            return event
        except Exception as e:
            print(f"Error creating event: {e}")
            raise e

    async def update_event(self, event_id: uuid.UUID, **update_data):
        try:
            # Fetch the current event
            event = await self.db.get(EventModel, event_id)
            if not event:
                return None

            # Update fields dynamically
            for key, value in update_data.items():
                setattr(event, key, value)

            # Commit the changes
            await self.db.commit()

            # Refresh the instance to get updated data
            await self.db.refresh(event)
            return event
        except Exception as e:
            await self.db.rollback()
            print(f"Error updating event: {e}")
            raise e

    async def delete_event(self, event_id: uuid.UUID):
        try:
            # Fetch the current event
            event = await self.db.get(EventModel, event_id)
            if not event:
                return None

            # Delete the event from the database
            await self.db.delete(event)
            await self.db.commit()

            return event

        except Exception as e:
            await self.db.rollback()
            print(f"Error deleting event: {e}")
            raise e

    async def get_event_with_on_going_status_with_receptionist_id(self, receptionist_id: str) -> list[dict]:
        try:
            query = select(EventModel).where(
                and_(
                    or_(EventModel.receptionist_1 == receptionist_id, EventModel.receptionist_2 == receptionist_id),
                    EventModel.status == "BERLANGSUNG"
                )
            )
            results = await self.db.execute(query)
            event = results.scalars().first()
            
            return event.to_dict()

        except Exception as e:
            print(f"Error fetching events: {e}")
