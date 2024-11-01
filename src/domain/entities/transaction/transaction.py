from dataclasses import dataclass
from datetime import datetime

@dataclass
class Transaction:
    transaction_id: str
    participant_id: str
    title: str
    amount: int
    category: str
    status: str
    created_at: datetime    
    updated_at: datetime