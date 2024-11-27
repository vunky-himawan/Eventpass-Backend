
from pydantic import BaseModel


class Receptionist(BaseModel):
    event_organizer_id: str
