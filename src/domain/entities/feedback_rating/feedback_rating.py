from dataclasses import dataclass
from datetime import datetime
from ..participant.participant import Participant
from ..event.event import Event

@dataclass
class FeedbackRating:
    feedback_rating_id: str
    participant: Participant
    event: Event
    rating_value: int
    rating_feedback: str
    created_at: datetime
    updated_at: datetime