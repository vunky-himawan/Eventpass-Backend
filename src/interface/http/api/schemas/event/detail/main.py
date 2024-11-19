import uuid
from pydantic import BaseModel

class EventDetailSchema(BaseModel):
    event_detail_id: uuid.UUID
    event_id: uuid.UUID
    event: dict
    event_receiptionist: dict
    speaker: dict
    employee: dict
