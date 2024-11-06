from pydantic import BaseModel, Field
from datetime import datetime
from pydantic.class_validators import validator

# Constants
ALLOWED_IMAGE_TYPES = ["image/jpeg", "image/png"]
MAX_FILE_SIZE = 1 * 1024 * 1024  # 1 MB dalam bytes

class ImageMetaData(BaseModel):
    """Schema untuk metadata gambar yang diupload"""
    filename: str
    content_type: str
    size: int
    uploaded_at: datetime = Field(default_factory=datetime.now)

class ImageUploadRequest(BaseModel):
    """Schema untuk validasi file upload"""
    file_extension: str = Field(..., description="Ekstensi file")
    file_data: bytes = Field(..., description="Data file")

    @validator('file_data')
    def validate_file_size(cls, v):
        """Validasi ukuran file"""
        if len(v) > MAX_FILE_SIZE:
            raise ValueError(
                f"Ukuran file terlalu besar. Maksimal: {MAX_FILE_SIZE/1024/1024:.1f}MB"
            )
        return v

    @validator('file_extension')
    def validate_file_extension(cls, v):
        """Validasi ekstensi file"""
        if v not in ALLOWED_IMAGE_TYPES:
            raise ValueError(
                f"Ekstensi file tidak diizinkan. Hanya: {', '.join(ALLOWED_IMAGE_TYPES)}"
            )
        return v