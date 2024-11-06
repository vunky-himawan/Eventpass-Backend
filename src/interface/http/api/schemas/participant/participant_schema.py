from pydantic import BaseModel
from fastapi import Form
from ......domain.entities.enum.gender import Gender

class Participant(BaseModel):
    participant_name: str
    age: int
    gender: Gender

    model_config = {
        "json_schema_extra": {
            "example": {
                "participant_name": "John Doe",
                "age": 30,
                "gender": "MALE"
            }
        }
    }

    @classmethod
    def as_form(cls,
                participant_name: str = Form(..., min_length=3, max_length=255, description="Name"),
                age: int = Form(..., ge=18, le=100, description="Age"),
                gender: Gender = Form(..., description="Gender")
    ): 
        return cls(
            participant_name=participant_name,
            age=age,
            gender=gender
        )