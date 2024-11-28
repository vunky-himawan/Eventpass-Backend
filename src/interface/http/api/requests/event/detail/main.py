
from typing import Optional
import uuid
from fastapi import Form
from pydantic import BaseModel, Field, model_validator


class EventDetailRequest(BaseModel):
    event_id: uuid.UUID
    speaker_id: Optional[uuid.UUID]
    event_receiptionist_id: uuid.UUID

    @model_validator(mode="before")
    def handle_empty_strings(cls, values):
        # Convert empty strings to None for speaker_id
        if values.get("speaker_id") == "":
            values["speaker_id"] = None
        return values

    @classmethod
    async def as_form(
        cls,
        event_id: uuid.UUID = Form(...),
        speaker_id: Optional[str] = Form(None),
        event_receiptionist_id: uuid.UUID = Form(...),
    ):
        return cls(
            event_id=event_id,
            speaker_id=speaker_id,
            event_receiptionist_id=event_receiptionist_id,
        )

class EventDetailUpdateRequest(BaseModel):
    event_id: Optional[uuid.UUID]
    speaker_id: Optional[uuid.UUID]
    event_receiptionist_id: Optional[uuid.UUID]

    @classmethod
    async def as_form(
            cls,
            event_id: Optional[uuid.UUID] = Form(None),
            speaker_id: Optional[uuid.UUID] = Form(None),
            event_receiptionist_id: Optional[uuid.UUID] = Form(None),
        ):
        return cls(
            event_id=event_id,
            speaker_id=speaker_id,
            event_receiptionist_id=event_receiptionist_id,
        )
