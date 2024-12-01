from datetime import datetime
from typing import Optional, Union
import uuid
from pydantic import BaseModel


class SpeakerSchema(BaseModel):
    speaker_id: Optional[Union[str, uuid.UUID]]
    name: str
    title: str
    social_media_links: str
    company: str
    created_at: Optional[datetime]
