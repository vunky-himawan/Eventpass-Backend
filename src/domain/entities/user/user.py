from datetime import datetime
from dataclasses import dataclass
from typing import Optional

@dataclass
class User:
    user_id: str 
    username: str
    email: str
    password: str
    role: str
    refresh_token: str | None = None
    profile_photo: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "username": self.username,
            "email": self.email,
            "refresh_token": self.refresh_token,
            "role": self.role,
            "profile_photo": self.profile_photo,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }
