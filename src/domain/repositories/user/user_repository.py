from abc import ABC, abstractmethod
from domain.entities.enum.role import Role
from domain.entities.user.user import User
from domain.entities.result.result import Result
from domain.entities.participant.participant import Participant
from domain.entities.event_organizer.event_organizer import EventOrganizer
from typing import List

from interface.http.api.schemas.event_organizer.receptionis.main import Receptionist

class UserRepository(ABC):
    @abstractmethod
    async def create_user(
            self, 
            username: str, 
            email: str,
            password: str, 
            role: Role, 
            feature_vector: bytes | None = None, 
            picture_path: str | None = None, 
            details: Participant | EventOrganizer | Receptionist | None = None
        ) -> Result[User]:
        pass

    @abstractmethod
    async def update_user(self, user: User) -> Result[User]:
        pass

    @abstractmethod
    async def update_user_details(self, user_id: str, details: Participant | EventOrganizer) -> Result[User | Participant | EventOrganizer]:
        pass

    @abstractmethod
    async def delete_user(self, user_id: str) -> Result[bool]:
        pass

    @abstractmethod
    async def get_user_details(self, user: User) -> Result[dict]:
        pass

    @abstractmethod
    async def upload_profile_photo(self, user_id: str, profile_photo: str) -> Result[bool]:
        pass

    @abstractmethod
    async def get_users(self, skip: int = 0, limit: int = 10) -> Result[list[User | Participant | EventOrganizer]]:
        pass

    @abstractmethod
    async def get_user_by_user_id(self, user_id: str) -> Result[dict]: 
        pass

    @abstractmethod
    async def get_user_by_username(self, username: str) -> Result[dict]: 
        pass
