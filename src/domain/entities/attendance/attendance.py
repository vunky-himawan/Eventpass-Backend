from dataclasses import dataclass
from datetime import datetime

@dataclass
class Attendance:
    event_attendance_id: str
    event_id: str
    receptionist_id: str
    participant_id: str
    ticket_id: str
    is_attended_in: bool
    attended_in_at: datetime
    is_attended_out: bool
    attended_out_at: datetime
    pin: str
    attendance_method: str
    status: str
    created_at: datetime    
    updated_at: datetime