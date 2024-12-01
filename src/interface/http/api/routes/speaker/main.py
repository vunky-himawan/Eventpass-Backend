import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.params.speaker.speaker_params import SpeakerParams
from src.domain.usecases.speaker.speaker_usecase import SpeakerUseCase
from src.infrastructure.config.database import get_db
from src.infrastructure.repositories.speaker.speaker_repository import SpeakerRepositoryImplementation
from src.interface.http.api.schemas.result.error_response import ErrorResponse
from src.interface.http.api.schemas.result.success_response import SuccessResponse


router = APIRouter()

def get_speaker_usecase(
        db: AsyncSession = Depends(get_db),
    )-> SpeakerUseCase:
    return SpeakerUseCase(
        speaker_repos=SpeakerRepositoryImplementation(db)
    )

@router.get(
    "/",
    response_model=SuccessResponse,
    responses={
        200: {"model": SuccessResponse},
        400: {"model": ErrorResponse},
        500: {"model": ErrorResponse}
    }
)
async def get(
    speaker_use_case: SpeakerUseCase = Depends(get_speaker_usecase),
    page: int = 1,
    page_size: int = 10
):
    if (page < 1):
        raise HTTPException(status_code=400, detail="Page must be greater than 0")
    if (page_size < 1):
        raise HTTPException(status_code=400, detail="Page size must be greater than 0")

    try:
        result = await speaker_use_case.call_get(SpeakerParams.Get(None, page, page_size))

        if "error" in result:
            raise Exception(result["error"])
        
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get(
    "/{speaker_id}",
    response_model=SuccessResponse,
    responses={
        200: {"model": SuccessResponse},
        400: {"model": ErrorResponse},
        500: {"model": ErrorResponse}
    }
)
async def find(
    speaker_id: uuid.UUID,
    speaker_use_case: SpeakerUseCase = Depends(get_speaker_usecase)
):
    try:
        result = await speaker_use_case.call_find(SpeakerParams.Find(speaker_id))
        
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get(
    "/search/{parameter}",
    response_model=SuccessResponse,
    responses={
        200: {"model": SuccessResponse},
        400: {"model": ErrorResponse},
        500: {"model": ErrorResponse}
    },
    description="Find speaker by name, title, or company"
)
async def find_by_name_or_title_or_company(
    parameter: str,
    speaker_use_case: SpeakerUseCase = Depends(get_speaker_usecase)
):
    try:
        result = await speaker_use_case.call_get(
            SpeakerParams.Get(parameter)
        )
        
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post(
    "/",
    response_model=SuccessResponse,
    responses={
        200: {"model": SuccessResponse},
        400: {"model": ErrorResponse},
        500: {"model": ErrorResponse}
    }
)
async def create(
    speaker_use_case: SpeakerUseCase = Depends(get_speaker_usecase),
    request: SpeakerParams.Create = Depends(SpeakerParams.Create.as_form)
):
    try:
        result = await speaker_use_case.call_create(request)

        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put(
    "/{speaker_id}",
    response_model=SuccessResponse,
    responses={
        200: {"model": SuccessResponse},
        400: {"model": ErrorResponse},
        500: {"model": ErrorResponse}
    }
)
async def update(
    speaker_id: uuid.UUID,
    speaker_use_case: SpeakerUseCase = Depends(get_speaker_usecase),
    request: SpeakerParams.Update = Depends(SpeakerParams.Update.as_form)
):
    try:
        result = await speaker_use_case.call_update(speaker_id, request)

        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete(
    "/{speaker_id}",
    responses={
        200: {"model": SuccessResponse},
        400: {"model": ErrorResponse},
        500: {"model": ErrorResponse}
    }
)
async def delete(
    speaker_id: uuid.UUID,
    speaker_use_case: SpeakerUseCase = Depends(get_speaker_usecase)
):
    try:
        result = await speaker_use_case.call_delete(SpeakerParams.Delete(speaker_id))

        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
