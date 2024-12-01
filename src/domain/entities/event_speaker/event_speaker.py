
from dataclasses import dataclass


@dataclass
class EventSpeaker:
    event_speaker_id: str
    event_id: str
    speaker_id: str

@dataclass
class EventSpeakerInput:
    event_speaker_id: str
    event_id: str
    speaker_id: str
