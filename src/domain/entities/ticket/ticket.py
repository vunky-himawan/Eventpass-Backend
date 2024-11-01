from dataclasses import dataclass
from datetime import datetime

@dataclass
class Ticket:
    ticket_id: str
    event_id: str
    transaction_id: str
    pin: str
    created_at: datetime
    updated_at: datetime