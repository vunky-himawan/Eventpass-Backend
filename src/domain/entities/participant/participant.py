from dataclasses import dataclass
from datetime import datetime

@dataclass
class Participant:
    participant_id: str
    user_id: str
    name: str
    age: int
    gender: str
    amount: int
    created_at: datetime
    updated_at: datetime