from pydantic import BaseModel, Field

class LoginRequest(BaseModel):
    username: str = Field(..., 
                         min_length=3, 
                         max_length=50, 
                         pattern="^[a-zA-Z0-9_]+$", 
                         description="Username")
    password: str = Field(..., 
                         min_length=8, 
                         max_length=255, 
                         pattern="^[a-zA-Z0-9_]+$", 
                         description="Password")
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "username": "john_doe",
                "password": "password123"
            }
        }
    }