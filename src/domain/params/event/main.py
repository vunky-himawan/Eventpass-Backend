from datetime import datetime
from typing import Optional
import uuid
from fastapi import UploadFile

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
            speaker_id: Optional[uuid.UUID],
            event_receiptionist_id: uuid.UUID,
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
        self.speaker_id = speaker_id    
        self.event_receiptionist_id = event_receiptionist_id

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
            speaker_id: Optional[uuid.UUID],
            event_receiptionist_id: uuid.UUID,
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
        self.speaker_id = speaker_id
        self.event_receiptionist_id = event_receiptionist_id
