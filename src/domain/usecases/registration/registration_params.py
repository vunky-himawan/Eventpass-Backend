from ...entities.participant.participant import Participant
from ...entities.event_organizer.event_organizer import EventOrganizer
from fastapi import UploadFile

class RegistrationParams:
    def __init__(self, username: str, password: str, email: str, role: str, face_photo: UploadFile | None = None, details: Participant | EventOrganizer | None = None):
        self.username = username
        self.password = password
        self.email = email
        self.role = role
        self.face_photo = face_photo
        self.details = details 