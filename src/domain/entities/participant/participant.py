from dataclasses import dataclass
from ..user.user import User
from datetime import datetime

@dataclass
class Participant: 
    participant_name: str  
    age: int   
    gender: str
    birth_date: str
    created_at: datetime 
    updated_at: datetime 
    participant_id: str | None = None 
    amount: int = 0 