
from abc import ABC, abstractmethod
from typing import Union

from src.domain.entities.speaker.speaker import Speaker
from src.infrastructure.database.models.speaker import SpeakerModel


class SpeakerRepository(ABC):
    @abstractmethod
    async def get_speaker(self, speaker_id: str) -> Union[SpeakerModel, None]:
        pass

    @abstractmethod
    async def get_all(self, current_page: int = 1, page_size: int = 10) -> list[SpeakerModel]:
        pass

    @abstractmethod
    async def create(
        self,
        name: str,
        title: str,
        social_media_links: str,
        company: str,
    ) -> Union[SpeakerModel, None]:
        pass

    @abstractmethod
    async def update(self, speaker_id: str, **update_data:Speaker)-> Union[Speaker, None]:
        pass

    @abstractmethod
    async def delete(self, speaker_id: str)-> bool:
        pass
