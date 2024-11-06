from pydantic import BaseModel, Field, constr
from pydantic.class_validators import validator
from pydantic.types import Annotated
from datetime import datetime
from typing import Optional

# Constants
MAX_FILE_SIZE = 1 * 1024 * 1024  # 1 MB dalam bytes

class ImageMetadata(BaseModel):
    """Schema untuk metadata gambar yang diupload"""
    filename: str
    content_type: str
    size: int
    uploaded_at: datetime = Field(default_factory=datetime.now)

class UploadResponse(BaseModel):
    """Schema untuk response sukses"""
    status: str = "success"
    message: str
    data: ImageMetadata
    status_code: int = 200

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

class FileUploadRequest(BaseModel):
    """Schema untuk validasi file upload"""
    file_name: str = Field(..., description="Nama file")
    file_data: bytes = Field(..., description="Data file")

    @validator('file_data')
    def validate_file_size(cls, v):
        """Validasi ukuran file"""
        if len(v) > MAX_FILE_SIZE:
            raise ValueError(
                f"Ukuran file terlalu besar. Maksimal: {MAX_FILE_SIZE/1024/1024:.1f}MB"
            )
        return v

class NameValidateRequest(BaseModel):
    """Schema untuk validasi nama file"""
    name: Annotated[str, constr(max_length=20, strip_whitespace=True)] = Field(
        ...,
        description="Nama untuk gambar (maksimal 20 karakter)",
        example="profile_pic"
    )

    @validator('name')
    def validate_name(cls, v):
        """Validasi nama file"""
        if not v.strip():
            raise ValueError("Nama tidak boleh kosong")
        if len(v) > 20:
            raise ValueError("Nama tidak boleh lebih dari 20 karakter")
        return v.strip()