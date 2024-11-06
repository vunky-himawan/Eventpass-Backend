from pydantic import BaseModel

class EventOrganizer(BaseModel):
    organization_name: str
    address: str
    phone_number: str
    email: str
    description: str