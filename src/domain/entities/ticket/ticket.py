from dataclasses import dataclass
from datetime import datetime
from ..event.event import Event
from ..transaction.transaction import Transaction

@dataclass
class Ticket:
    ticket_id: str
    event: Event
    transaction: Transaction
    pin: str
    created_at: datetime
    updated_at: datetime