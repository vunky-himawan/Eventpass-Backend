
from typing import Optional
import uuid


class EventDetailCreationParams:
    def __init__(
            self,
            event_id: uuid.UUID,
            event_receiptionist_id: uuid.UUID,
            speaker_id: Optional[uuid.UUID]
        ):
        self.event_id = event_id
        self.event_receiptionist_id = event_receiptionist_id
        self.speaker_id = speaker_id

class EventDetailUpdateParams:
    def __init__(
            self,
            event_id: Optional[uuid.UUID],
            event_receiptionist_id: Optional[uuid.UUID],
            speaker_id: Optional[uuid.UUID],    
        ):
        self.event_id = event_id
        self.event_receiptionist_id = event_receiptionist_id
        self.speaker_id = speaker_id
