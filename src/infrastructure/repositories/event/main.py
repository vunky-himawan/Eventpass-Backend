import uuid
from domain.params.event.main import EventCreationParams
from infrastructure.database.models.event import  EventModel

class EventRepositoryImplementation:
    def __init__(self, db):
        self.db = db

    async def get_event(self, event_id:str):
        try:
            events = await self.db.get(EventModel, event_id)
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

