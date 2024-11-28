
from typing import Optional
import uuid
from infrastructure.database.models.event_detail import EventDetailModel
from sqlalchemy.future import select


class EventDetailRepositoryImplementation:
    def __init__(self, db):
        self.db = db

    async def get_event_detail(self, event_detail_id:uuid.UUID):
        try:
            events = await self.db.get(EventDetailModel, event_detail_id)
            return events
        except Exception as e:
            print(f"Error fetching events: {e}")
            raise e

    async def get_event_detail_by_event_id(self, event_id: uuid.UUID) -> EventDetailModel:
        try:
            event_detail = await self.db.get(EventDetailModel, event_id)
            return event_detail
        except Exception as e:
            print(f"Error fetching event detail by event id: {e}")
            raise e

    async def create_event_detail(
            self,
            event_id: uuid.UUID | str,
            event_receiptionist_id: uuid.UUID,
            speaker_id: Optional[uuid.UUID] = None
        ) -> EventDetailModel:
        try:
            event_detail = EventDetailModel(
                    event_id=event_id,
                    event_receiptionist_id=event_receiptionist_id,
                    speaker_id=speaker_id
            )
            self.db.add(event_detail)
            await self.db.commit()
            await self.db.refresh(event_detail)
            return event_detail
        except Exception as e:
            print(f"Error creating event detail: {e}")
            raise e

    async def update_event_detail(self, event_detail_id: uuid.UUID, **update_data) -> EventDetailModel:
        try:
            # Fetch the current event
            event_detail = await self.db.get(EventDetailModel, event_detail_id)
            if not event_detail:
                raise Exception("Event detail tidak ditemukan")

            # Update fields dynamically
            for key, value in update_data.items():
                setattr(event_detail, key, value)

            # Commit the changes
            await self.db.commit()

            # Refresh the instance to get updated data
            await self.db.refresh(event_detail)
            return event_detail

        except Exception as e:
            await self.db.rollback()
            print(f"Error updating event detail: {e}")
            raise e

    async def delete_event_detail(self, event_detail_id: uuid.UUID) -> EventDetailModel:
        try:
            # Fetch the current event
            event_detail = await self.db.get(EventDetailModel, event_detail_id)
            if not event_detail:
                raise Exception("Event detail not found")

            # Delete the event from the database
            await self.db.delete(event_detail)
            await self.db.commit()

            return event_detail

        except Exception as e:
            await self.db.rollback()
            print(f"Error deleting event detail: {e}")
            raise e