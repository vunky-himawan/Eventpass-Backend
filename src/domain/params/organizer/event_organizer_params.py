from datetime import datetime
from typing import Optional
import uuid

from fastapi import Form


class EventOrganizerParams:
    class Create:
        user_id: uuid.UUID
        organization_name: str
        address: str
        phone_number: str
        email: str
        description: str
        amount: int

        def __init__(
                self,
                user_id: uuid.UUID,
                organization_name: str,
                address: str,
                phone_number: str,
                email: str,
                description: str,
                amount: int = 0,
        ):
            self.user_id = user_id
            self.organization_name = organization_name
            self.address = address
            self.phone_number = phone_number
            self.email = email
            self.description = description
            self.amount = amount

        @classmethod
        def as_form(
                cls,
                user_id: uuid.UUID,
                organization_name: str,
                address: str,
                phone_number: str,
                email: str,
                description: str,
                amount: int = 0,
        ):
            return cls(
                user_id=user_id,
                organization_name=organization_name,
                address=address,
                phone_number=phone_number,
                email=email,
                description=description,
                amount=amount,
            )
    
    class Update:
        user_id: Optional[uuid.UUID]
        organization_name: Optional[str]
        address: Optional[str]
        phone_number: Optional[str]
        email: Optional[str]
        description: Optional[str]
        amount: Optional[int]

        def __init__(
                self,
                user_id: Optional[uuid.UUID],
                organization_name: Optional[str],
                address: Optional[str],
                phone_number: Optional[str],
                email: Optional[str],
                description: Optional[str],
                amount: Optional[int] = 0,
        ):
            self.user_id = user_id
            self.organization_name = organization_name
            self.address = address
            self.phone_number = phone_number
            self.email = email
            self.description = description
            self.amount = amount

        @classmethod
        def as_form(
                cls,
                user_id: Optional[uuid.UUID] = Form(None),
                organization_name: Optional[str]= Form(None),
                address: Optional[str]= Form(None),
                phone_number: Optional[str]= Form(None),
                email: Optional[str]= Form(None),
                description: Optional[str]= Form(None),
                amount: Optional[int] = Form(None),
        ):
            return cls(
                user_id=user_id,
                organization_name=organization_name,
                address=address,
                phone_number=phone_number,
                email=email,
                description=description,
                amount=amount,
            )

    class Delete:
        event_organizer_id: uuid.UUID
        def __init__(self, event_organizer_id: uuid.UUID):
            self.event_organizer_id = event_organizer_id

        @classmethod
        def as_form(cls, event_organizer_id: uuid.UUID):
            return cls(event_organizer_id=event_organizer_id)

    class Find:
        organizer_id: uuid.UUID | str

        def __init__(
                self, 
                organizer_id: uuid.UUID | str
        ): 
            self.organizer_id = organizer_id

    class Get:
        parameter: Optional[str]
        page: int = 1
        page_size: int = 10

        def __init__(
                self,
                parameter: Optional[str],
                page: int = 1,
                page_size: int = 10,
        ):
            self.parameter = parameter
            self.page = page
            self.page_size = page_size
