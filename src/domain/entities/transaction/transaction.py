from dataclasses import dataclass
from datetime import datetime
from ..participant.participant import Participant

@dataclass
class Transaction:
    transaction_id: str
    participant: Participant
    title: str
    amount: int
    category: str
    status: str
    created_at: datetime    
    updated_at: datetime