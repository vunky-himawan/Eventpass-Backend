from pydantic import BaseModel
from typing import Optional

class ErrorResponse(BaseModel):
    """Schema untuk response error"""
    status: str = "error"
    message: str
    detail: Optional[str] = None
    status_code: int = 400

    def to_response(self):
        """Convert to FastAPI response format"""
        return {
            "status": self.status,
            "message": self.message,
            "detail": self.detail,
            "status_code": self.status_code
        }