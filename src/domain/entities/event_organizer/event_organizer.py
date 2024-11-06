from dataclasses import dataclass
from datetime import datetime
from ..user.user import User

@dataclass
class EventOrganizer:
    organization_name: str
    address: str
    phone_number: str
    email: str
    description: str
    created_at: datetime
    updated_at: datetime
    event_organizer_id: str | None = None
    amount: int = 0