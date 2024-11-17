from dataclasses import dataclass
from datetime import datetime
from domain.entities.participant.participant import Participant

@dataclass
class FacePhoto:
    face_photo_id: str
    participant: Participant
    picture_path: str
    created_at: datetime