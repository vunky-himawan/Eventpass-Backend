from typing import Generic, Optional, TypeVar, Union, List
from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)

class SuccessResponse(BaseModel, Generic[T]):
    """Schema untuk response sukses"""
    status: str = "success"
    message: str
    data: Optional[Union[dict, List[dict]]] = None
    status_code: int = 200

    def to_response(self):
        """Convert to FastAPI response format"""
        return {
            "status": self.status,
            "message": self.message,
            "data": self.data,
            "status_code": self.status_code
        }
