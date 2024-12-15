from typing import Optional
import uuid
from datetime import datetime

from sqlalchemy.orm import selectinload
from infrastructure.database.models.event import EventModel
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import String, and_, cast, func, or_
from domain.repositories.event.main import EventRepository


class EventRepositoryImplementation(EventRepository):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_upcoming_events(self, current_page: int = 1, page_size: int = 10) -> list[dict]:
        try:
            today = datetime.today()
            query = select(EventModel).where(
                EventModel.start_date >= today
            ).order_by(
                EventModel.start_date.asc()
            ).options(
                selectinload(EventModel.event_speakers),
                selectinload(EventModel.event_organizer)
            ).limit(
                page_size
            ).offset((current_page - 1) * page_size)

            events = await self.db.execute(query)
            return events.scalars().all()

        except ValueError as e:
            print(f"Error fetching events: {e}")
            raise e
        except Exception as e:
            print(f"Error fetching events: {e}")
            raise e


    async def get_all(self, current_page: int = 1, page_size: int = 10):
        try:
            query = select(EventModel).order_by(
                    EventModel.created_at.desc()
                    ).options(
                        selectinload(EventModel.event_speakers),
                        selectinload(EventModel.event_organizer)
                    ).limit(
                            page_size
                    ).offset((current_page - 1) * page_size)

            events = await self.db.execute(query)
            return events.scalars().all()
        except Exception as e:
            print(f"Error fetching events: {e}")
            raise e

    async def get_count_all(self):
        try:
            query = select(func.count(EventModel.event_id)).select_from(EventModel)

            count = await self.db.execute(query)
            return count.scalars().first()
        except Exception as e:
            print(f"Error fetching events: {e}")
            raise e

    async def get_event(self, event_id:str | uuid.UUID):
        try:
            if isinstance(event_id, str):
                event_id = uuid.UUID(event_id)

            query = select(EventModel).where(cast(EventModel.event_id, String) == str(event_id))

            events = await self.db.execute(query)

            event = events.scalars().first()
            if event is None:
                return None;

            return event
        except Exception as e:
            print(f"Error fetching events: {e}")
            raise e

    async def get_all_by_title_or_type_or_status(self, title_or_type: str):
        try:
            query = select(EventModel).where(
                or_(
                    EventModel.title.ilike(f"%{title_or_type}%"),
                    EventModel.type.ilike(f"%{title_or_type}%"),
                    EventModel.status.ilike(f"%{title_or_type}%")
                )
            )

            results = await self.db.execute(query)
            events = results.scalars().all()
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
                raise Exception("Event not found")

            # Update fields dynamically
            for key, value in update_data.items():
                setattr(event, key, value)

            print(f"Updated attributes: {update_data}")
            # Commit the changes
            await self.db.commit()

            # Refresh the instance to get updated data
            await self.db.refresh(event)
            return event
        except Exception as e:
            print(f"Error updating event: {e}")
            await self.db.rollback()
            raise e

    async def delete_event(self, event_id: uuid.UUID):
        try:
            event = await self.db.get(EventModel, event_id)
            if not event:
                raise Exception("Event not found")

            await self.db.delete(event)
            await self.db.commit()

            return event

        except Exception as e:
            await self.db.rollback()
            print(f"Error deleting event: {e}")
            raise e

    async def get_event_with_on_going_status_with_receptionist_id(self, receptionist_id: str) -> dict:
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

    async def substract_ticket(self, event_id: uuid.UUID) -> bool:
        try:
            event = await self.db.get(EventModel, event_id)

            if not event:
                return False
            
            event.ticket_quantity -= 1
            await self.db.commit()
            await self.db.refresh(event)
            return True

        except ValueError as e:
            await self.db.rollback()
            raise e
        except Exception as e:
            await self.db.rollback()
            raise e
