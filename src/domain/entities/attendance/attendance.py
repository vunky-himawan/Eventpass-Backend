from dataclasses import dataclass
from datetime import datetime
from ..event.event import Event
from ..user.user import User as Receptionist
from ..participant.participant import Participant
from ..enum.status import Status

@dataclass
class Attendance:
    event_attendance_id: str
    event: Event
    receptionist: Receptionist
    participant: Participant
    ticket_id: str
    attended_in_at: datetime
    attended_out_at: datetime
    pin: str
    attendance_method: str
    status: Status
    created_at: datetime    
    updated_at: datetime