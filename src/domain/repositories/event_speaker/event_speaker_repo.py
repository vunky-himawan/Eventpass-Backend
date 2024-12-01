from abc import ABC, abstractmethod
from typing import List
import uuid

from src.infrastructure.database.models.event_speaker import EventSpeakerModel


class EventSpeakerRepository(ABC):
    @abstractmethod
    async def get_event_speaker(self, event_id: str) -> List[EventSpeakerModel]:
        pass
    
    @abstractmethod
    async def create(self, event_id: uuid.UUID, speaker_id: uuid.UUID) -> EventSpeakerModel:
        pass

    @abstractmethod
    async def update(self, event_speaker_id: uuid.UUID, **update_data: EventSpeakerModel) -> EventSpeakerModel:
        pass

    @abstractmethod
    async def delete(self, event_speaker_id: uuid.UUID) -> EventSpeakerModel:
        pass

