from dataclasses import dataclass
from datetime import datetime
from ..event.event import Event
from ..user.user import User as Receptionist
from ..participant.participant import Participant
from ..enum.status import Status

@dataclass
class Attendance:
    event_attendance_id: str
    event_id: str
    receptionist_id: str
    participant_id: str
    attended_in_at: datetime
    attendance_method: str
    status: Status
    created_at: datetime    
    updated_at: datetime

    def to_dict(self):
        return {
            "event_attendance_id": self.event_attendance_id,
            "event_id": self.event_id,
            "receptionist_id": self.receptionist_id,
            "participant_id": self.participant_id,
            "attended_in_at": self.attended_in_at,
            "attendance_method": self.attendance_method,
            "status": self.status,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }