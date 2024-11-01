from datetime import datetime
from dataclasses import dataclass

@dataclass
class User:
    user_id: str
    username: str
    email: str
    password: str
    role: str
    profile_photo: str
    created_at: datetime
    updated_at: datetime