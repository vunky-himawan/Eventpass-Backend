from dataclasses import dataclass
from datetime import datetime
from ..event_organizer.event_organizer import EventOrganizer

@dataclass
class Event:
    event_id: str
    event_organizer: EventOrganizer
    thumbnail_path: str
    title: str
    address: str
    description: str
    type: str
    status: str
    ticket_price: int
    ticket_quantity: int
    start_date: datetime
    created_at: datetime
    updated_at: datetime