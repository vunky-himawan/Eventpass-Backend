from dataclasses import dataclass
from datetime import datetime

@dataclass
class Notification:
    notification_id: str
    user_id: str
    type: str
    for_model: str
    data: str
    read_at: datetime
    created_at: datetime