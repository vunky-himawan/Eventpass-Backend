import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from domain.params.event.main import EventCreationParams, UpdateEventParams
from domain.usecases.event.main import EventCreationUseCase, EventDeleteUseCase, EventUpdateUseCase
from infrastructure.config.database import get_db
from infrastructure.repositories.event.main import EventRepositoryImplementation
from infrastructure.services.image_service import ImageService
from interface.http.api.requests.event.main import EventCreationRequest, UpdateEventRequest
from interface.http.api.schemas.event.main import EventSchema
from interface.http.api.schemas.result.error_response import ErrorResponse
from interface.http.api.schemas.result.success_response import SuccessResponse

router = APIRouter()

def get_event_creation_usecase(db: AsyncSession = Depends(get_db)) -> EventCreationUseCase:
    image_service = ImageService(storage_directory='uploads/event')
    event_repository = EventRepositoryImplementation(db)
    
    return EventCreationUseCase(
        image_service=image_service,
        event_repository=event_repository
    )

def get_event_update_usecase(db: AsyncSession = Depends(get_db)) -> EventUpdateUseCase:
    image_service = ImageService(storage_directory='uploads/event')
    event_repository = EventRepositoryImplementation(db)
    
    return EventUpdateUseCase(
        image_service=image_service,
        event_repository=event_repository
    )

def get_event_delete_usecase(db: AsyncSession = Depends(get_db)) -> EventDeleteUseCase:
    event_repository = EventRepositoryImplementation(db)
    
    return EventDeleteUseCase(
        event_repository=event_repository
    )

@router.post(
    "/", 
    response_model=SuccessResponse[EventSchema],
    responses={
        200: {"model": SuccessResponse[EventSchema]},
        400: {"model": ErrorResponse},
        500: {"model": ErrorResponse}
    }
)
async def create_event(
            request: EventCreationRequest = Depends(EventCreationRequest.as_form),
            event_creation_use_case: EventCreationUseCase = Depends(get_event_creation_usecase)
        ):
    params = EventCreationParams(
        title=request.title,
        thumbnail=request.thumbnail,
        address=request.address,
        description=request.description,
        type=request.type.name,
        status=request.status.value,
        ticket_price=request.ticket_price,
        ticket_quantity=request.ticket_quantity,
        start_date=request.start_date,
        event_organizer_id=request.event_organizer_id
    )

    result = await event_creation_use_case.call(params)

    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])

    event_data = result["event"]
    return SuccessResponse(
        status="success",
        message="Event created successfully",
        data=event_data,
        status_code=200
    )

@router.put(
    "/{event_id}",
    response_model=SuccessResponse[UpdateEventRequest],
    responses={
        200: {"model": SuccessResponse[UpdateEventRequest]},
        400: {"model": ErrorResponse},
        500: {"model": ErrorResponse}
    }
)
async def update_event(
    event_id: uuid.UUID,
    request: UpdateEventRequest = Depends(UpdateEventRequest.as_form),
    event_update_use_case: EventUpdateUseCase = Depends(get_event_update_usecase)
):
    params = UpdateEventParams(
        title=request.title,
        address=request.address,
        description=request.description,
        type=request.type,
        status=request.status,
        ticket_price=request.ticket_price,
        ticket_quantity=request.ticket_quantity,
        start_date=request.start_date,
        event_organizer_id=request.event_organizer_id,
        thumbnail=request.thumbnail
    )

    try:
        result = await event_update_use_case.call(event_id, params)

        print(result)
        event_data = result["event"]
        return SuccessResponse(
            status="success",
            message="Event updated successfully",
            data=event_data,
            status_code=200
        )
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=str(e))

@router.delete(
    "/{event_id}",
    response_model=SuccessResponse[UpdateEventRequest],
    responses={
        200: {"model": SuccessResponse[UpdateEventRequest]},
        400: {"model": ErrorResponse},
        500: {"model": ErrorResponse}
    }
)
async def delete_event(
    event_id: uuid.UUID,
    event_delete_use_case: EventDeleteUseCase = Depends(get_event_delete_usecase)
):
    result = await event_delete_use_case.call(event_id)

    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])

    return SuccessResponse(
        status="success",
        message="Event deleted successfully",
        data=None,
        status_code=200
    )
