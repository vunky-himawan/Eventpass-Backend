from domain.repositories.face_recognition.face_recognition_repository import FaceRecognitionRepository
from sqlalchemy.ext.asyncio import AsyncSession
import uuid
from infrastructure.database.models.face_photos import FacePhotoModel
from sqlalchemy import select

class FaceRecognitionRepositoryImplementation(FaceRecognitionRepository):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_face_embedding_by_participant_id(self, participant_id: str | uuid.UUID) -> dict:
        try:
            query = select(FacePhotoModel).where(FacePhotoModel.participant_id == participant_id)
            result = await self.db.execute(query)
            face_data = result.scalars().first()

            return face_data.to_dict()

        except Exception as e:
            print(f"Error fetching face recognition data: {e}")
            raise e