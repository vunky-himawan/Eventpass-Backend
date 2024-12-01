import uuid
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.entities.speaker.speaker import Speaker
from src.domain.repositories.speaker.speaker_repo import SpeakerRepository
from src.infrastructure.database.models.speaker import SpeakerModel

class SpeakerRepositoryImplementation(SpeakerRepository):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(
            self,
            name: str,
            title: str,
            social_media_links: str,
            company: str,
    ):
        try:
            prepared_speaker = SpeakerModel(
                name=name,
                title=title,
                social_media_links=social_media_links,
                company=company,
            )

            self.db.add(prepared_speaker)
            await self.db.commit()
            await self.db.refresh(prepared_speaker)
            return prepared_speaker
        except Exception:
            await self.db.rollback()
            raise Exception("Failed to create speaker")
    
    async def update(
            self,
            speaker_id: uuid.UUID | str,
            **update_data
    ):
        print(f"Updating speaker with id: {speaker_id}")
        try:
            speaker = await self.db.get(SpeakerModel, speaker_id)
            if not speaker:
                raise Exception("Speaker not found")

            # Update fields dynamically
            for key, value in update_data.items():
                setattr(speaker, key, value)

            # Commit the changes
            await self.db.commit()

            # Refresh the instance to get updated data
            await self.db.refresh(speaker)
            return speaker
        except Exception as e:
            await self.db.rollback()
            print(e)
            raise Exception("Failed to update speaker")

    async def delete(self, speaker_id: uuid.UUID | str):
        try:
            speaker = await self.db.get(SpeakerModel, speaker_id)
            if not speaker:
                raise Exception("Speaker not found")

            await self.db.delete(speaker)
            await self.db.commit()
            return True
        except Exception:
            await self.db.rollback()
            raise Exception("Failed to delete speaker")

    async def get_all(self):
        try:
            speakers = await self.db.execute(select(SpeakerModel))
            entities = [SpeakerModel.to_entity(speaker) for speaker in speakers]
            return entities
        except Exception:
            await self.db.rollback()
            raise Exception("Failed to get all speakers")

    async def get_speaker(self, speaker_id: str):
        try:
            speaker = await self.db.get(SpeakerModel, speaker_id)
            if not speaker:
                return None
            return speaker
        except Exception:
            await self.db.rollback()
            raise Exception("Failed to get speaker")

