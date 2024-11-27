from datetime import datetime
from typing import Optional
import uuid
from pydantic import BaseModel, field_validator
from fastapi import Form, File, UploadFile

from interface.http.api.schemas.event.main import EventStatusEnum, EventTypeEnum

class EventCreationRequest(BaseModel):
    title: str
    thumbnail: UploadFile
    address: str
    description: str
    type: EventTypeEnum
    status: EventStatusEnum
    ticket_price: int
    ticket_quantity: int
    start_date: datetime
    event_organizer_id: str
    speaker_id: Optional[uuid.UUID | str]
    event_receiptionist_id: uuid.UUID

    @field_validator('speaker_id', mode='before')
    def validate_speaker_id(cls, v):
        if v == "":
            return None
        return v

    @classmethod
    async def as_form(
        cls,
        title: str = Form(...),
        address: str = Form(...),
        description: str = Form(...),
        type: EventTypeEnum = Form(...),
        status: EventStatusEnum = Form(...),
        ticket_price: int = Form(0),
        ticket_quantity: int = Form(0),
        start_date: datetime = Form(...),
        thumbnail: UploadFile = File(...),
        event_organizer_id: str = Form(...),
        speaker_id: Optional[uuid.UUID | str] = Form(None),
        event_receiptionist_id: uuid.UUID = Form(...),
    ):
        return cls(
                title=title, 
                thumbnail=thumbnail,
                address=address,
                description=description,
                type=type,
                status=status,
                ticket_price=ticket_price,
                ticket_quantity=ticket_quantity,
                start_date=start_date,
                event_organizer_id=event_organizer_id,
                speaker_id=speaker_id,
                event_receiptionist_id=event_receiptionist_id,
        )

class UpdateEventRequest(BaseModel):
    title: Optional[str]
    address: Optional[str]
    description: Optional[str]
    type: Optional[EventTypeEnum]
    status: Optional[EventStatusEnum]
    ticket_price: Optional[int]
    ticket_quantity: Optional[int]
    start_date: Optional[datetime]
    event_organizer_id: Optional[str]
    thumbnail: Optional[UploadFile]
    speaker_id: Optional[uuid.UUID]
    event_receiptionist_id: uuid.UUID
    speaker_id: Optional[uuid.UUID]
    event_receiptionist_id: uuid.UUID

    @classmethod
    async def as_form(
        cls,
        title: Optional[str] = Form(None),  # Optional, defaults to None
        address: Optional[str] = Form(None),  # Optional, defaults to None
        description: Optional[str] = Form(None),  # Optional, defaults to None
        type: Optional[EventTypeEnum] = Form(None),  # Optional, defaults to None
        status: Optional[EventStatusEnum] = Form(None),  # Optional, defaults to None
        ticket_price: Optional[int] = Form(None),  # Optional, defaults to None
        ticket_quantity: Optional[int] = Form(None),  # Optional, defaults to None
        start_date: Optional[datetime] = Form(None),  # Optional, defaults to None
        event_organizer_id: Optional[str] = Form(None),  # Optional, defaults to None
        thumbnail: Optional[UploadFile] = File(None),  # Optional, defaults to None
        speaker_id: Optional[uuid.UUID] = Form(None),
        event_receiptionist_id: uuid.UUID = Form(...),

    ):
        return cls(
            title=title,
            address=address,
            description=description,
            type=type,
            status=status,
            ticket_price=ticket_price,
            ticket_quantity=ticket_quantity,
            start_date=start_date,
            event_organizer_id=event_organizer_id,
            thumbnail=thumbnail,
            speaker_id=speaker_id,
            event_receiptionist_id=event_receiptionist_id,
        )
