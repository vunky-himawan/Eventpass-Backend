from dataclasses import dataclass
from datetime import datetime

@dataclass
class Speaker:
    speaker_id: str
    name: str
    title: str
    social_media_links: str
    company: str
    created_at: datetime

@dataclass
class SpeakerInput:
    name: str
    title: str
    social_media_links: str
    company: str

@dataclass
class SpeakerOutput:
    speaker_id: str
    name: str
    title: str
    social_media_links: str
    company: str
