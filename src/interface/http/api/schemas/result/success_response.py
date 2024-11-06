from pydantic import BaseModel
from typing import Optional

class SuccessResponse(BaseModel):
    """Schema untuk response sukses"""
    status: str = "success"
    message: str
    data: Optional[dict] = None
    status_code: int = 200

    def to_response(self):
        """Convert to FastAPI response format"""
        return {
            "status": self.status,
            "message": self.message,
            "data": self.data,
            "status_code": self.status_code
        }