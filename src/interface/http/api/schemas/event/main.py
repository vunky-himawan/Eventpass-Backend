import uuid
from pydantic import BaseModel
from datetime import datetime
from enum import Enum

from interface.http.api.schemas.event.detail.main import EventDetailSchema


class EventStatusEnum(str, Enum):
    BUKA = "BUKA"
    TUTUP = "TUTUP"
    SELESAI = "SELESAI"


class EventTypeEnum(str, Enum):
    KONVERENSI = "KONFERENSI"
    WORKSHOP = "WORKSHOP"
    FESTIVAL = "FESTIVAL"
    LAINNYA = "LAINNYA"
    EXPO = "EXPO"
    KONVENSI = "KONVENSI"

class EventSchema(BaseModel):
    event_id: str
    event_organizer_id: str
    thumbnail_path: str 
    title: str
    address: str
    description: str
    type: str
    status: str
    ticket_price: int
    ticket_quantity: int
    start_date: datetime

class LocalDetail (BaseModel):
        event_id: uuid.UUID
        event_receiptionist: dict
        speaker: str
        employee: dict

class EventWithDetailSchema(EventSchema):
    detail: LocalDetail
