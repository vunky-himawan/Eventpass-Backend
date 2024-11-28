from domain.entities.participant.participant import Participant
from domain.entities.event_organizer.event_organizer import EventOrganizer
from fastapi import UploadFile

from interface.http.api.schemas.event_organizer.receptionis.main import Receptionist

class RegistrationParams:
    def __init__(self, 
                 username: str, 
                 password: str,
                 email: str, 
                 role: str,
                 face_photo: UploadFile | None = None, 
                 details: Participant | EventOrganizer | Receptionist | None = None
    ):
        self.username = username
        self.password = password
        self.email = email
        self.role = role
        self.face_photo = face_photo
        self.details = details 
