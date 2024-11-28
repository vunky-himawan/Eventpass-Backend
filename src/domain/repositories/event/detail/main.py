from abc import ABC, abstractmethod
import uuid
from infrastructure.database.models.event_detail import EventDetailModel

class EventDetailRepository(ABC):
    @abstractmethod
    async def delete_event_detail(self, event_detail_id: uuid.UUID) -> EventDetailModel:
        pass

    @abstractmethod
    async def update_event_detail(self, event_detail_id: uuid.UUID, **update_data) -> EventDetailModel:
        pass

    @abstractmethod
    async def create_event_detail(self, event_id: uuid.UUID, event_receiptionist_id: uuid.UUID, speaker_id: uuid.UUID) -> EventDetailModel:
        pass

    @abstractmethod
    async def get_event_detail_by_event_id(self, event_id: uuid.UUID) -> EventDetailModel:
        pass

    @abstractmethod
    async def get_event_detail(self, event_detail_id:uuid.UUID):
        pass

    @abstractmethod
    async def get_event_by_receptionist_id(self, receptionist_id: str) -> list[EventDetailModel]:
        pass