from datetime import datetime
from typing import List, Optional
import uuid
from fastapi import UploadFile

from src.domain.entities.event_speaker.event_speaker import EventSpeakerInput
from src.domain.entities.speaker.speaker import Speaker

class EventCreationParams:
    def __init__(
            self,
            title: str,
            address: str,
            description: str,
            type: str,
            status: str,
            ticket_price: int,
            ticket_quantity: int,
            start_date: datetime,
            thumbnail: UploadFile,
            event_organizer_id: str,
            receptionist_1: uuid.UUID,
            receptionist_2: Optional[uuid.UUID] = None,
            
            speaker: List[Speaker] = [],
    ):
        self.title = title
        self.thumbnail = thumbnail
        self.address = address
        self.description = description
        self.type = type
        self.status = status
        self.ticket_price = ticket_price
        self.ticket_quantity = ticket_quantity
        self.start_date = start_date
        self.event_organizer_id = event_organizer_id

        self.speaker = speaker

        self.receptionist_1 = receptionist_1
        self.receptionist_2 = receptionist_2

class UpdateEventParams:
    def __init__(
            self,
            title: Optional[str],
            address: Optional[str],
            description: Optional[str],
            type: Optional[str],
            status: Optional[str],
            ticket_price: Optional[int],
            ticket_quantity: Optional[int],
            start_date: Optional[datetime],
            event_organizer_id: Optional[str],
            thumbnail: Optional[UploadFile],

            speaker: Optional[List[EventSpeakerInput]] = None,

            receptionist_1: Optional[uuid.UUID] = None,
            receptionist_2: Optional[uuid.UUID] = None,
        ):
        self.title = title
        self.address = address
        self.description = description
        self.type = type
        self.status = status
        self.ticket_price = ticket_price
        self.ticket_quantity = ticket_quantity
        self.start_date = start_date
        self.event_organizer_id = event_organizer_id
        self.thumbnail = thumbnail

        self.speaker = speaker

        self.receptionist_1 = receptionist_1
        self.receptionist_2 = receptionist_2
