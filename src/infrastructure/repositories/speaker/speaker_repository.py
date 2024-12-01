import uuid
from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.entities.speaker.speaker import Speaker
from src.domain.params.speaker.speaker_params import SpeakerParams
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

            for key, value in update_data.items():
                setattr(speaker, key, value)

            await self.db.commit()
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
            return speaker
        except Exception:
            await self.db.rollback()
            raise Exception("Failed to delete speaker")

    async def get_all(
        self,
        current_page: int = 1,
        page_size: int = 10
    ):
        try:
            query = select(SpeakerModel).order_by(
                    SpeakerModel.created_at.desc()
                    ).limit(
                            page_size
                    ).offset((current_page - 1) * page_size)
            speakers = await self.db.execute(query)
            return speakers.scalars().all()
        except Exception as e:
            await self.db.rollback()
            raise Exception("Failed to get all speakers\n" + str(e))

    async def get_by_name_or_title_or_company(self, params: SpeakerParams.Get):
        try:
            query = select(SpeakerModel).where(or_(
                SpeakerModel.name.ilike(f"%{params.parameter}%"),
                SpeakerModel.title.ilike(f"%{params.parameter}%"),
                SpeakerModel.company.ilike(f"%{params.parameter}%")
            )).limit(params.page_size).offset((params.page - 1) * params.page_size)
            speaker = await self.db.execute(query)
            return speaker.scalars().all()
        except Exception as e:
            await self.db.rollback()
            raise Exception("Failed to get speakers by name, title, or company\n" + str(e))

    async def get_speaker(self, speaker_id: str | uuid.UUID):
        try:
            speaker = await self.db.get(SpeakerModel, speaker_id)
            if not speaker:
                return None
            return speaker
        except Exception:
            await self.db.rollback()
            raise Exception("Failed to get speaker")
    
    async def find(self, speaker_id: uuid.UUID | str):
        try:
            speaker = await self.db.get(SpeakerModel, speaker_id)
            if not speaker:
                raise Exception("Speaker not found")
            return speaker
        except Exception:
            await self.db.rollback()
            raise Exception("Failed to find speaker")
