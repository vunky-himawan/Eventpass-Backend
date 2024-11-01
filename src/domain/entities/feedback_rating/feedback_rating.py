from dataclasses import dataclass
from datetime import datetime

@dataclass
class FeedbackRating:
    feedback_rating_id: str
    participant_id: str
    event_id: str
    rating_value: int
    rating_feedback: str
    created_at: datetime
    updated_at: datetime