from abc import ABC, abstractmethod
import uuid

class FaceRecognitionRepository(ABC):
    @abstractmethod
    async def get_face_embedding_by_participant_id(self, participant_id: str | uuid.UUID) -> dict:
        pass