from datetime import datetime, date
from pydantic import BaseModel, model_validator
from fastapi import Form
from domain.entities.enum.gender import Gender


class Participant(BaseModel):
    participant_name: str
    age: int
    gender: Gender
    birth_date: str

    # Custom schema example for documentation
    model_config = {
        "json_schema_extra": {
            "example": {
                "participant_name": "John Doe",
                "age": 30,
                "gender": "MALE",
                "birth_date": "2000-01-01" 
            }
        }
    }

    @classmethod
    def as_form(cls,
                participant_name: str = Form(..., min_length=3, max_length=255, description="Name"),
                age: int = Form(..., ge=18, le=100, description="Age"),
                gender: Gender = Form(..., description="Gender"),
                birth_date: str = Form(..., description="Birth date in 'YYYY-MM-DD' format")  # Use string for input
    ): 
        # Convert birth_date string to a datetime.date object
        birth_date_obj = datetime.strptime(birth_date, "%Y-%m-%d").date()
        return cls(
            participant_name=participant_name,
            age=age,
            gender=gender,
            birth_date=birth_date_obj
        )
