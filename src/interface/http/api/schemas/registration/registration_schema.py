from pydantic import BaseModel, ValidationError
from interface.http.api.schemas.participant.participant_schema import Participant
from interface.http.api.schemas.event_organizer.event_organizer_schema import EventOrganizer
from fastapi import HTTPException
from typing import Optional, Union, Set
from fastapi import Form, File, UploadFile
import json
import imghdr

class RegistrationRequest(BaseModel):
    username: str
    password: str
    email: str
    role: str
    face_photo: Optional[UploadFile] = None
    details: Optional[Union[Participant, EventOrganizer]] = None

    @classmethod
    async def as_form(cls,
        username: str = Form(..., min_length=3, max_length=50, regex="^[a-zA-Z0-9_]+$", description="Username", example="john_doe"),
        password: str = Form(..., min_length=8, max_length=255, regex="^[a-zA-Z0-9_]+$", description="Password", example="password123"),
        email: str = Form(..., min_length=3, max_length=100, regex="^[a-zA-Z0-9_.]+@[a-zA-Z0-9_.]+.[a-zA-Z]+$", description="Email address", example="john.doe@example.com"),
        role: str = Form(..., example="PARTICIPANT"),
        face_photo: Optional[UploadFile] = File(None, description="Profile photo"),
        details: Optional[str] = Form(None, example='{"name": "John Doe", "address": "123 Main St", "phone_number": "555-1234", "email": "john.doe@example.com", "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit."}')
    ): 
        if face_photo:
            try:
                cls.validate_image_file(face_photo)
            except HTTPException as e:
                raise ValueError(e.detail)
            except Exception as e:
                raise ValueError(f"Error validating image file: {str(e)}")

        # Parse details JSON if provided
        parsed_details = None
        if details:
            try:
                details_dict = json.loads(details)
                if role == "PARTICIPANT":
                    parsed_details = Participant(**details_dict)
                elif role == "EVENT_ORGANIZER":
                    parsed_details = EventOrganizer(**details_dict)
            except (json.JSONDecodeError, ValidationError) as e:
                raise ValueError(f"Invalid details format: {str(e)}")

        return cls(
            username=username,
            password=password,
            email=email,
            role=role,
            face_photo=face_photo,
            details=parsed_details
        )
    
    @staticmethod
    def validate_image_file(file: UploadFile) -> None:
        """Validate image file size and format"""
        # Check file size (2MB limit)
        MAX_FILE_SIZE = 2 * 1024 * 1024  # 2MB in bytes
        ALLOWED_EXTENSIONS: Set[str] = {'jpg', 'jpeg', 'png'}
        
        # Read file content
        file_content = file.file.read()
        file.file.seek(0)  # Reset file pointer after reading
        
        # Validate file size
        if len(file_content) > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=400,
                detail=f"File size exceeds maximum limit of 2MB. Current size: {len(file_content) / (1024 * 1024):.2f}MB"
            )
        
        # Get file extension from filename
        file_ext = file.filename.rsplit('.', 1)[-1].lower() if '.' in file.filename else ''
        if file_ext not in ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid file extension. Allowed extensions are: {', '.join(ALLOWED_EXTENSIONS)}"
            )
        
        # Validate actual file content type using imghdr
        image_format = imghdr.what(None, h=file_content)
        if image_format not in ['jpeg', 'png']:
            raise HTTPException(
                status_code=400,
                detail="Invalid image format. Only JPEG and PNG formats are allowed"
            )
