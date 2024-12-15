from typing import Generic, Optional, TypeVar, Any
from pydantic import BaseModel
from typing import Generic, Optional, TypeVar 

T = TypeVar("T", bound=BaseModel)

class SuccessResponse(BaseModel, Generic[T]):
    """Schema untuk response sukses"""
    status: str = "success"
    message: str
    data: Optional[Any] = None
    status_code: int = 200

    def to_response(self):
        """Convert to FastAPI response format"""
        return {
            "status": self.status,
            "message": self.message,
            "data": self.data,
            "status_code": self.status_code
        }
