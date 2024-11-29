from datetime import datetime
from typing import List, Optional, Union
import uuid
from json_repair import json_repair
from pydantic import BaseModel, Field, field_validator, model_validator, validator
from fastapi import Form, File, UploadFile

from interface.http.api.schemas.event.main import EventStatusEnum, EventTypeEnum
from src.domain.entities.speaker.speaker import Speaker
from src.interface.http.api.schemas.speaker.speaker_schema import SpeakerSchema

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
    receptionist_1: uuid.UUID
    receptionist_2: Optional[uuid.UUID]

    speaker: str

    @field_validator("receptionist_2", mode="before")
    def validate_receptionist_2(cls, v):
        if v == "":
            return None  # Convert empty string to None
        return v  # Let Pydantic handle the validation for UUIDs

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
        receptionist_1: uuid.UUID = Form(...),
        receptionist_2: Optional[uuid.UUID] = Form(None),

        speaker: str = Form(...,example={"name": "John Doe", "title": "Speaker", "social_media_links": "https://twitter.com/johndoe", "company": "Company Name"}),
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
                receptionist_1=receptionist_1,
                receptionist_2=receptionist_2,

                speaker=speaker,
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
    receptionist_1: Optional[uuid.UUID]
    receptionist_2: Optional[uuid.UUID]

    speaker: Optional[List[str]]

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
        receptionist_1: Optional[uuid.UUID] = Form(None),
        receptionist_2: Optional[uuid.UUID] = Form(None),

        speaker: Optional[List[str]] = Form(None),
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
            receptionist_1=receptionist_1,
            receptionist_2=receptionist_2,

            speaker=speaker,
        )
