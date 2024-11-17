from abc import ABC, abstractmethod
from domain.entities.participant.participant import Participant

class ParticipantRepository(ABC):
    @abstractmethod
    async def get_participants(self, skip: int = 0, limit: int = 10) -> list[Participant]:
        pass

    @abstractmethod
    async def get_participant_by_id(self, participant_id: str) -> Participant:
        pass

    @abstractmethod
    async def get_participant_by_name(self, participant_name: str) -> Participant:
        pass

    @abstractmethod
    async def create_participant(self, participant: Participant) -> Participant:
        pass

    @abstractmethod
    async def update_participant(self, participant: Participant) -> Participant:
        pass

    @abstractmethod
    async def delete_participant(self, participant_id: str) -> bool:
        pass

    @abstractmethod
    async def add_participant_to_event(self, participant_id: str, event_id: str) -> bool:
        pass

    @abstractmethod
    async def remove_participant_from_event(self, participant_id: str, event_id: str) -> bool:
        pass

    @abstractmethod
    async def check_participant_in_event(self, participant_id: str, event_id: str) -> bool:
        pass