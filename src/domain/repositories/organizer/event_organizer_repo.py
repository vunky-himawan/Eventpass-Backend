from abc import ABC, abstractmethod
from typing import Sequence
import uuid

from src.domain.params.organizer.event_organizer_params import EventOrganizerParams
from src.infrastructure.database.models.event_organizer import EventOrganizerModel


class EventOrganizerRepository(ABC):
    @abstractmethod
    async def create(self, params: EventOrganizerParams.Create) -> dict:
        pass
    
    @abstractmethod
    async def update(self, event_organizer_id: str, **update_data: EventOrganizerParams.Update) -> EventOrganizerModel:
        pass
    
    @abstractmethod
    async def delete(self, params: EventOrganizerParams.Delete) -> EventOrganizerModel:
        pass
    
    @abstractmethod
    async def get_all(self, params: EventOrganizerParams.Get) -> Sequence[EventOrganizerModel]:
        pass

    @abstractmethod
    async def find(self, params: EventOrganizerParams.Find) -> EventOrganizerModel:
        pass

    @abstractmethod
    async def get_by_name_or_email(self, params: EventOrganizerParams.Get) -> Sequence[EventOrganizerModel]:
         pass
