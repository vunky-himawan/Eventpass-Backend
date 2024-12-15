from fastapi import Form
from pydantic import BaseModel, Field

class ChangePasswordRequest(BaseModel):
    old_password: str = Field(..., description="Password lama")
    new_password: str = Field(..., description="Password baru")

    model_config = {
        "json_schema_extra": {
            "example": {
                "old_password": "123456",
                "new_password": "654321"
            }
        }
    }