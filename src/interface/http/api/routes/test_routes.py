from fastapi import APIRouter, UploadFile, HTTPException, status, Form, File
from ..schemas.test.upload import UploadResponse, ErrorResponse, ImageMetadata, FileUploadRequest, NameValidateRequest
from .....infrastructure.services.image_service import ImageService
from bcrypt import hashpw, gensalt
import bcrypt

router = APIRouter()
ALLOWED_IMAGE_TYPES = ["image/jpeg", "image/png", "image/gif"]

@router.post(
    "/upload/image",
    response_model=UploadResponse,
    responses={
        400: {"model": ErrorResponse},
        500: {"model": ErrorResponse}
    }
)
async def test_upload_file(
    name: str = Form(...),
    image: UploadFile = File(...)
) -> UploadResponse:
    """
    Endpoint untuk upload gambar
    """
    try:
        # Validasi nama
        try:
            validated_name = NameValidateRequest(name=name)
        except ValueError as name_error:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=ErrorResponse(
                    message="Validasi nama gagal",
                    detail=str(name_error),
                    status_code=400
                ).to_response()
            )

        # Validasi tipe file
        if image.content_type not in ALLOWED_IMAGE_TYPES:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=ErrorResponse(
                    message="Tipe file tidak diizinkan",
                    detail=f"Tipe yang diizinkan: {', '.join(ALLOWED_IMAGE_TYPES)}",
                    status_code=400
                ).to_response()
            )

        # Baca dan validasi file
        try:
            contents = await image.read()
            validated_request = FileUploadRequest(
                file_name=image.filename,
                file_data=contents
            )
        except ValueError as file_error:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=ErrorResponse(
                    message="Validasi file gagal",
                    detail=str(file_error),
                    status_code=400
                ).to_response()
            )

        # Reset file pointer
        await image.seek(0)

        # Buat metadata response
        image_metadata = ImageMetadata(
            filename=image.filename,
            content_type=image.content_type,
            size=len(contents)
        )

        # Return success response
        return UploadResponse(
            message="File berhasil diupload",
            data=image_metadata
        )

    except HTTPException as http_exc:
        # Re-raise HTTP exceptions as they already have the correct format
        raise http_exc

    except Exception as e:
        # Handle unexpected errors
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=ErrorResponse(
                message="Terjadi kesalahan internal",
                detail=str(e),
                status_code=500
            ).to_response()
        )
    
@router.post('/face-detection')
async def face_detection(image: UploadFile = File(...)):
    try:
        image_service = ImageService(storage_directory="uploads/dataset")
        face_photo_path = image_service.save_face_data(image, image.filename, 'vunky')

        return {"message": "Face detection successful", "face_photo_path": face_photo_path}
    
    except ValueError as value_error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ErrorResponse(
                message="Validasi file gagal",
                detail=str(value_error),
                status_code=400
            ).to_response()
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=ErrorResponse(
                message="Terjadi kesalahan internal",
                detail=str(e),
                status_code=500
            ).to_response()
        )
    
@router.post('/passowrd')
async def password(password: str = Form(...)):
    try:
        alamak = '123456'
        hash_password = bcrypt.hashpw(alamak.encode('utf-8'), bcrypt.gensalt())

        compare_password = bcrypt.hashpw(password.encode('utf-8'), hash_password)

        if compare_password != hash_password:
            raise ValueError("Password salah")

        return {"message": "Password successful", "password": hash_password}
    
    except ValueError as value_error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ErrorResponse(
                message="Validasi file gagal",
                detail=str(value_error),
                status_code=400
            ).to_response()
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=ErrorResponse(
                message="Terjadi kesalahan internal",
                detail=str(e),
                status_code=500
            ).to_response()
        )