from dataclasses import dataclass
from datetime import datetime

@dataclass
class FaceEmbedding:
    face_embedding_id: str
    participant_id: str
    picture_path: str
    feature_vector: str
    created_at: datetime