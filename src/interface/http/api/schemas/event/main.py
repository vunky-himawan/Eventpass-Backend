import uuid
from pydantic import BaseModel
from datetime import datetime
from enum import Enum


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
