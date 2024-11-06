from dataclasses import dataclass
from datetime import datetime
from ..user.user import User

@dataclass
class Notification:
    notification_id: str
    user: User
    type: str
    for_model: str
    data: str
    read_at: datetime
    created_at: datetime