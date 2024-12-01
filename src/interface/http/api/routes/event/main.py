from datetime import datetime
import logging
import os
import uuid
from fastapi import APIRouter, Depends, HTTPException
from json_repair import json_repair
from sqlalchemy.ext.asyncio import AsyncSession

from domain.params.event.main import EventCreationParams, UpdateEventParams
from domain.usecases.event.main import EventCreationUseCase, EventDeleteUseCase, EventGetUseCase, EventUpdateUseCase
from infrastructure.config.database import get_db
from infrastructure.repositories.event.main import EventRepositoryImplementation
from infrastructure.services.image_service import ImageService
from interface.http.api.requests.event.main import EventCreationRequest, UpdateEventRequest
from interface.http.api.schemas.result.error_response import ErrorResponse
from interface.http.api.schemas.result.success_response import SuccessResponse
from src.domain.entities.event_speaker.event_speaker import EventSpeaker, EventSpeakerInput
from src.domain.entities.speaker.speaker import Speaker, SpeakerInput
from src.infrastructure.repositories.event_speaker.event_speaker_repos import EventSpeakerRepositoryImplementation
from src.infrastructure.repositories.speaker.speaker_repository import SpeakerRepositoryImplementation
from src.interface.http.api.schemas.event.main import EventSchema
router = APIRouter()

static_dir = os.getenv("STATIC_DIR", "dist")
logger = logging.getLogger('uvicorn.error')

def get_event_creation_usecase(db: AsyncSession = Depends(get_db)) -> EventCreationUseCase:
    image_service = ImageService(storage_directory=os.path.join("uploads/event"))
    event_repository = EventRepositoryImplementation(db)
    speaker_repos = SpeakerRepositoryImplementation(db)
    event_speaker_repos = EventSpeakerRepositoryImplementation(db)
    
    return EventCreationUseCase(
        image_service=image_service,
        event_repository=event_repository,
        speaker_repos=speaker_repos,
        event_speaker_repos=event_speaker_repos,
    )

def get_event_update_usecase(db: AsyncSession = Depends(get_db)) -> EventUpdateUseCase:
    image_service = ImageService(storage_directory=os.path.join(static_dir, "uploads/event"))
    event_repository = EventRepositoryImplementation(db)
    speaker_repos = SpeakerRepositoryImplementation(db)
    event_speaker_repos = EventSpeakerRepositoryImplementation(db)

    return EventUpdateUseCase(
        image_service=image_service,
        event_repository=event_repository,
        speaker_repos=speaker_repos,
        event_speaker_repos=event_speaker_repos,
    )

def get_event_delete_usecase(db: AsyncSession = Depends(get_db)) -> EventDeleteUseCase:
    event_repository = EventRepositoryImplementation(db)
    
    return EventDeleteUseCase(
        event_repository=event_repository
    )

def get_event_get_usecase(db: AsyncSession = Depends(get_db)) -> EventGetUseCase:
    event_repository = EventRepositoryImplementation(db)

    return EventGetUseCase(
            event_repository=event_repository
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
async def get_events(
        event_get_use_case: EventGetUseCase = Depends(get_event_get_usecase),
        page: int = 1,
        page_size: int = 10
):
    if (page < 1):
        raise HTTPException(status_code=400, detail="Page must be greater than 0")
    if (page_size < 1):
        raise HTTPException(status_code=400, detail="Page size must be greater than 0")

    result = await event_get_use_case.call(current_page=page, page_size=page_size)

    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])

    return SuccessResponse(
        status="success",
        message="Events retrieved successfully",
        data=result["data"],
        status_code=200
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
    speakers = []
    if request.speaker:
        jsn = json_repair.loads(request.speaker)
        speaker_attributes = ["name", "title", "social_media_links", "company"]

        if type(jsn) == list:
            for speaker in jsn:
                if all(key in speaker for key in speaker_attributes):
                    parsed_speaker = SpeakerInput(**speaker)

                    if not isinstance(parsed_speaker, SpeakerInput):
                        raise HTTPException(status_code=400, detail="Speaker must be a Speaker object")
                   
                    entity_speaker = Speaker(
                        speaker_id="",
                        name=parsed_speaker.name,
                        title=parsed_speaker.title,
                        social_media_links=parsed_speaker.social_media_links,
                        company=parsed_speaker.company,
                        created_at=datetime.now()
                    )
                    speakers.append(entity_speaker)
                else:
                    raise HTTPException(status_code=400, detail="Speaker must have name, title, social_media_links, company")
        else:
            raise HTTPException(status_code=400, detail="Speaker must be a list")

    try:
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
            event_organizer_id=request.event_organizer_id,
            receptionist_1=request.receptionist_1,
            receptionist_2=request.receptionist_2,
            speaker=speakers,
        )

        result = await event_creation_use_case.call(params)

        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])

        event_data = result["data"]
        return SuccessResponse(
            status="success",
            message="Event created successfully",
            data=event_data,
            status_code=200
        )
    except Exception as e:
        return ErrorResponse(status_code=400, message=str(e))
        

@router.put(
    "/{event_id}",
    response_model=SuccessResponse,
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
    speakers = []
    if request.speaker:
        jsn = json_repair.loads(request.speaker)
        speaker_attributes = ["event_speaker_id", "speaker_id", "event_id"]

        if type(jsn) == list:
            for speaker in jsn:
                if all(key in speaker for key in speaker_attributes):
                    parsed_speaker = EventSpeakerInput(**speaker)

                    if not isinstance(parsed_speaker, EventSpeakerInput):
                        raise HTTPException(status_code=400, detail=f"Speaker must contain {speaker_attributes}")
                   
                    entity_speaker = EventSpeaker(
                        event_speaker_id=parsed_speaker.event_speaker_id,
                        event_id=parsed_speaker.event_id,
                        speaker_id=parsed_speaker.speaker_id
                    )
                    speakers.append(entity_speaker)
                else:
                    raise HTTPException(status_code=400, detail="Speaker must have name, title, social_media_links, company")
        else:
            raise HTTPException(status_code=400, detail="Speaker must be a list")

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
        thumbnail=request.thumbnail,
        receptionist_1=request.receptionist_1,
        receptionist_2=request.receptionist_2,

        speaker=speakers,
    )

    try:
        result = await event_update_use_case.call(event_id, params)

        event_data = result["data"]
        return SuccessResponse(
            status="success",
            message=result["message"],
            data=event_data,
            status_code=200
        )
    except Exception as e:
        print(e)
        if e == "Event tidak ditemukan":
            raise HTTPException(status_code=404, detail={"error": str(e)})
        else:
            raise HTTPException(status_code=400, detail={"error": str(e)})

@router.delete(
    "/{event_id}",
    responses={
        200: {"model": SuccessResponse},
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
        if result["error"] == "Event tidak ditemukan":
            raise HTTPException(status_code=404, detail=result["error"])
        else:
            raise HTTPException(status_code=400, detail=result["error"])

    return SuccessResponse(
        status="success",
        message=result["message"],
        data={ "content": result["event"] },
        status_code=200
    )
