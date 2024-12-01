
import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.params.organizer.event_organizer_params import EventOrganizerParams
from src.domain.usecases.organizer.event_organizer_usecase import EventOrganizerUseCase
from src.infrastructure.config.database import get_db
from src.infrastructure.repositories.organizer.event_organizer_repo_implements import EventOrganizerRepositoryImplementation
from src.interface.http.api.schemas.result.error_response import ErrorResponse
from src.interface.http.api.schemas.result.success_response import SuccessResponse


router = APIRouter()

def get_organizer_usecase(
        db: AsyncSession = Depends(get_db)
) -> EventOrganizerUseCase:
    event_organizer_repos = EventOrganizerRepositoryImplementation(db)
    return EventOrganizerUseCase(event_organizer_repos)

@router.get(
    "/",
    response_model=SuccessResponse,
    responses={
        200: {"model": SuccessResponse},
        400: {"model": ErrorResponse},
        500: {"model": ErrorResponse}
    }
)
async def get_organizers(
    organizer_get_use_case: EventOrganizerUseCase = Depends(get_organizer_usecase),
    page: int = 1,
    page_size: int = 10
):
    if (page < 1):
        raise HTTPException(status_code=400, detail="Page must be greater than 0")
    if (page_size < 1):
        raise HTTPException(status_code=400, detail="Page size must be greater than 0")
    
    try:
        params = EventOrganizerParams.Get(page=page, page_size=page_size, parameter=None)
        result = await organizer_get_use_case.call_get(params)

        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])

        return SuccessResponse(
            status="success",
            message="Organizers retrieved successfully",
            data=result["data"],
            status_code=200
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get(
    "/{organizer_id}",
    response_model=SuccessResponse,
    responses={
        200: {"model": SuccessResponse},
        400: {"model": ErrorResponse},
        500: {"model": ErrorResponse}
    }
)
async def get_organizer(
    organizer_id: uuid.UUID,
    organizer_get_use_case: EventOrganizerUseCase = Depends(get_organizer_usecase)
):
    try:
        result = await organizer_get_use_case.call_find(EventOrganizerParams.Find(organizer_id=organizer_id))

        return SuccessResponse(
            status="success",
            message="Organizer retrieved successfully",
            data=result["data"],
            status_code=200
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get(
    "/search/{name_or_email}",
    response_model=SuccessResponse,
    responses={
        200: {"model": SuccessResponse},
        400: {"model": ErrorResponse},
        500: {"model": ErrorResponse}
    }
)
async def search_organizers(
    name_or_email: str,
    organizer_get_use_case: EventOrganizerUseCase = Depends(get_organizer_usecase),
    page: int = 1,
    page_size: int = 10
):
    try:
        params = EventOrganizerParams.Get(page=page, page_size=page_size, parameter=name_or_email)
        result = await organizer_get_use_case.call_get(params)

        return SuccessResponse(
            status="success",
            message="Organizers retrieved successfully",
            data=result["data"],
            status_code=200
        )
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
async def create_organizer(
        organizer_create_use_case: EventOrganizerUseCase = Depends(get_organizer_usecase),
        request: EventOrganizerParams.Create = Depends(EventOrganizerParams.Create.as_form)
):
    try:
        result = await organizer_create_use_case.call_create(request)

        return SuccessResponse(
            status="success",
            message="Organizer created successfully",
            data=result["data"],
            status_code=200
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put(
    "/{organizer_id}",
    response_model=SuccessResponse,
    responses={
        200: {"model": SuccessResponse},
        400: {"model": ErrorResponse},
        500: {"model": ErrorResponse}
    }
)
async def update_organizer(
    organizer_id: uuid.UUID,
    organizer_update_use_case: EventOrganizerUseCase = Depends(get_organizer_usecase),
    request: EventOrganizerParams.Update = Depends(EventOrganizerParams.Update.as_form)
):
    try:
        result = await organizer_update_use_case.call_update(organizer_id, request)

        return SuccessResponse(
            status="success",
            message="Organizer updated successfully",
            data=result["data"],
            status_code=200
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete(
    "/{organizer_id}",
    response_model=SuccessResponse,
    responses={
        200: {"model": SuccessResponse},
        400: {"model": ErrorResponse},
        500: {"model": ErrorResponse}
    }
)
async def delete_organizer(
    organizer_delete_use_case: EventOrganizerUseCase = Depends(get_organizer_usecase),
    request: EventOrganizerParams.Delete = Depends(EventOrganizerParams.Delete.as_form)
):
    try:
        result = await organizer_delete_use_case.call_delete(request)

        return SuccessResponse(
            status="success",
            message="Organizer deleted successfully",
            data=result["data"],
            status_code=200
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
