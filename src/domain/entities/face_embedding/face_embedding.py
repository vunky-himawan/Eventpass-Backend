from dataclasses import dataclass
from datetime import datetime
from ..participant.participant import Participant

@dataclass
class FaceEmbedding:
    face_embedding_id: str
    participant: Participant
    picture_path: str
    feature_vector: bytes
    created_at: datetime