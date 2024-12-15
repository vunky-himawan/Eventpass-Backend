from abc import ABC, abstractmethod
from domain.entities.participant.participant import Participant
import uuid

class ParticipantRepository(ABC):
    @abstractmethod
    async def subtract_balance(self, participant_id: str | uuid.UUID, amount: int) -> bool:
        pass

    @abstractmethod
    async def add_balance(self, participant_id: str | uuid.UUID, amount: int) -> bool:
        pass

    @abstractmethod
    async def get_participant_by_participant_id(self, participant_id: str | uuid.UUID) -> Participant:
        pass

    @abstractmethod
    async def get_participant_by_user_id(self, user_id: str | uuid.UUID) -> Participant:
        pass

    @abstractmethod
    async def get_participant_by_username(self, username: str) -> dict:
        pass