from abc import ABC, abstractmethod
from domain.entities.enum.role import Role
from domain.entities.user.user import User
from domain.entities.result.result import Result
from domain.entities.participant.participant import Participant
from domain.entities.event_organizer.event_organizer import EventOrganizer
from typing import List

class UserRepository(ABC):
    @abstractmethod
    async def create_user(self, username: str, email: str, password: str, role: Role, face_photo_paths: List[str] | None = None, details: Participant | EventOrganizer | None = None) -> Result[User]:
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
    async def get_user_details(self, user: User) -> Result[None | Participant | EventOrganizer]:
        pass

    @abstractmethod
    async def upload_profile_photo(self, user_id: str, profile_photo: str) -> Result[bool]:
        pass

    @abstractmethod
    async def get_users(self, skip: int = 0, limit: int = 10) -> Result[list[User | Participant | EventOrganizer]]:
        pass
