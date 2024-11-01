from dataclasses import dataclass
from datetime import datetime

@dataclass
class EventOrganizer:
    event_organizer_id: str
    user_id: str
    name: str
    address: str
    phone_number: str
    email: str
    description: str
    amount: int
    created_at: datetime
    updated_at: datetime