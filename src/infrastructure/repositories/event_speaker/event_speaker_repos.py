import uuid
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.domain.repositories.event_speaker.event_speaker_repo import EventSpeakerRepository
from src.infrastructure.database.models.event_speaker import EventSpeakerModel


class EventSpeakerRepositoryImplementation(EventSpeakerRepository):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_event_speaker(self, event_id: uuid.UUID | str):
        try:
            query = await self.db.execute(
                    select(EventSpeakerModel)
                        .where(
                            EventSpeakerModel.event_id == event_id
                        )
                    )
            return [EventSpeakerModel.to_entity(event_speaker) for event_speaker in query]
        except Exception:
            raise Exception("Failed to get event speaker")
    
    async def create(self, event_id: uuid.UUID | str, speaker_id: uuid.UUID | str):
        try:
            event_speaker = EventSpeakerModel(
                event_id=event_id,
                speaker_id=speaker_id
            )
            self.db.add(event_speaker)
            await self.db.commit()
            await self.db.refresh(event_speaker)
            return event_speaker
        except Exception as e:
            await self.db.rollback()
            print(f"Error creating event speaker: {e}")
            raise Exception("Failed to create event speaker")

    async def update(self, event_speaker_id: uuid.UUID, **update_data):
        try:
            event_speaker = await self.db.get(EventSpeakerModel, event_speaker_id)
            if not event_speaker:
                raise Exception("Event speaker not found")

            for key, value in update_data.items():
                setattr(event_speaker, key, value)

            await self.db.commit()

            await self.db.refresh(event_speaker)
            return event_speaker
        except Exception as e:
            await self.db.rollback()
            print(f"Error updating event speaker: {e}")
            raise Exception("Failed to update event speaker")

    async def delete(self, event_speaker_id: uuid.UUID | str):
        try:
            event_speaker = await self.db.get(EventSpeakerModel, event_speaker_id)
            if not event_speaker:
                raise Exception("Event speaker not found")

            await self.db.delete(event_speaker)
            await self.db.commit()
            return event_speaker
        except Exception:
            await self.db.rollback()
            raise Exception("Failed to delete event speaker")
