from fastapi import UploadFile, File, Form
from pydantic import BaseModel
from enum import Enum

class AttendanceRequest(BaseModel):
    photo: UploadFile
    receptionist_id: str

    @classmethod
    async def as_form(
        cls,
        photo: UploadFile = File(...),
        receptionist_id: str = Form(...),
    ):
        return cls(
            photo=photo, 
            receptionist_id=receptionist_id,
        )
    
    
class FaceAttendanceConfirmationRequest(BaseModel):
    is_correct: bool
    event_id: str
    receptionist_id: str
    participant_username: str
    
    @classmethod
    async def as_form(
        cls,
        is_correct: bool = Form(...),
        receptionist_id: str = Form(...),
        event_id: str = Form(...),
        participant_username: str = Form(...),
    ):
        return cls(
            is_correct=is_correct,
            receptionist_id=receptionist_id,
            event_id=event_id,
            participant_username=participant_username,
        )
    
class PinAttendanceConfirmationRequest(BaseModel):
    pin: str
    receptionist_id: str
    
    @classmethod
    async def as_form(
        cls,
        pin: str = Form(...),
        receptionist_id: str = Form(...),
    ):
        return cls(
            pin=pin,
            receptionist_id=receptionist_id,
        )