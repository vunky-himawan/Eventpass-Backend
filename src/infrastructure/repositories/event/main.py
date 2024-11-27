import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from infrastructure.database.models.event import  EventModel
from infrastructure.database.models.event_detail import EventDetailModel
from infrastructure.database.models.event_employee import EventEmployeeModel

class EventRepositoryImplementation:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self):
        try:
            events = await self.db.execute(
                    select(EventModel)
                    .order_by(EventModel.created_at.desc())
                    .options(
                        selectinload(EventModel.event_details)
                            .selectinload(EventDetailModel.employee)
                    )
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
            return events
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
            start_date: str
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
                    start_date=start_date
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

