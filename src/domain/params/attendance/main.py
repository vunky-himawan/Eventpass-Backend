from fastapi import UploadFile

class AttendanceParams:
    def __init__(self, photo: UploadFile, receptionist_id: str):
        self.photo = photo
        self.receptionist_id = receptionist_id

class FaceAttendanceConfirmationParams:
    def __init__(self, is_correct: bool, receptionist_id: str, participant_username: str, event_id: str):
        self.is_correct = is_correct
        self.receptionist_id = receptionist_id
        self.participant_username = participant_username
        self.event_id = event_id

class PinAttendanceConfirmationParams:
    def __init__(self, pin: str, receptionist_id: str):
        self.pin = pin
        self.receptionist_id = receptionist_id