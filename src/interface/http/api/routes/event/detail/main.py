
# import uuid
# from fastapi import APIRouter, Depends, HTTPException
# from sqlalchemy.ext.asyncio import AsyncSession

# from domain.params.event.detail.main import EventDetailCreationParams, EventDetailUpdateParams
# from domain.usecases.event.detail.main import EventDetailCreationUseCase, EventDetailDeleteUseCase, EventDetailUpdateUseCase
# from infrastructure.config.database import get_db
# from infrastructure.repositories.event.detail.main import EventDetailRepositoryImplementation
# from infrastructure.repositories.event.main import EventRepositoryImplementation
# from interface.http.api.requests.event.detail.main import EventDetailRequest, EventDetailUpdateRequest
# from interface.http.api.schemas.event.detail.main import EventDetailSchema
# from interface.http.api.schemas.result.error_response import ErrorResponse
# from interface.http.api.schemas.result.success_response import SuccessResponse


# router = APIRouter()

# def get_event_detail_creation_usecase(db: AsyncSession = Depends(get_db)) -> EventDetailCreationUseCase:
#     event_detail_repository = EventDetailRepositoryImplementation(db)
#     event_repository = EventRepositoryImplementation(db)
    
#     return EventDetailCreationUseCase(
#         event_repository=event_repository,
#         event_detail_repository=event_detail_repository
#     )

# def get_event_detail_update_usecase(db: AsyncSession = Depends(get_db)) -> EventDetailUpdateUseCase:
#     event_repository = EventDetailRepositoryImplementation(db)
    
#     return EventDetailUpdateUseCase(
#         event_repository
#     )

# def get_event_detail_delete_usecase(db: AsyncSession = Depends(get_db)) -> EventDetailDeleteUseCase:
#     event_repository = EventDetailRepositoryImplementation(db)
    
#     return EventDetailDeleteUseCase(
#         event_repository
#     )

# @router.post(
#     "/",
#     response_model=SuccessResponse[EventDetailSchema],
#     responses={
#         200: {"model": SuccessResponse[EventDetailSchema]},
#         400: {"model": ErrorResponse},
#         500: {"model": ErrorResponse}
#     }
# )
# async def create_event_detail(
#             request: EventDetailRequest = Depends(EventDetailRequest.as_form),
#             event_detail_creation_use_case: EventDetailCreationUseCase = Depends(get_event_detail_creation_usecase)
#         ):
#     params = EventDetailCreationParams(
#                             event_id=request.event_id,
#                             event_receiptionist_id=request.event_receiptionist_id,
#                             speaker_id=request.speaker_id
#                         )
#     try:
#         result = await event_detail_creation_use_case.call(request.event_id, params)

#         event_data = result["event"]
#         return SuccessResponse(
#             status="success",
#             message="Event created successfully",
#             data=event_data,
#             status_code=200
#         )
#     except Exception as e:
#         print(e)
#         if "not found" in str(e):
#             raise HTTPException(status_code=404, detail={"error": str(e)})
#         else:
#             raise HTTPException(status_code=400, detail={"error": str(e)})

# @router.put(
#     "/{event_detail_id}",
#     response_model=SuccessResponse[EventDetailSchema],
#     responses={
#         200: {"model": SuccessResponse[EventDetailSchema]},
#         400: {"model": ErrorResponse},
#         500: {"model": ErrorResponse}
#     }
# )
# async def update_event_detail(
#     event_detail_id: uuid.UUID,
#     request: EventDetailUpdateRequest = Depends(EventDetailUpdateRequest.as_form),
#     event_detail_update_use_case: EventDetailUpdateUseCase = Depends(get_event_detail_update_usecase)
# ):
#     params = EventDetailUpdateParams(
#                             event_id=request.event_id,
#                             event_receiptionist_id=request.event_receiptionist_id,
#                             speaker_id=request.speaker_id
#                         )
#     try:
#         result = await event_detail_update_use_case.call(event_detail_id, params)

#         event_data = result["event"]
#         return SuccessResponse(
#             status="success",
#             message="Event updated successfully",
#             data=event_data,
#             status_code=200
#         )
#     except Exception as e:
#         print(e)
#         if "not found" in str(e):
#             raise HTTPException(status_code=404, detail={"error": str(e)})
#         else:
#             raise HTTPException(status_code=400, detail={"error": str(e)})

# @router.delete(
#     "/{event_detail_id}",
#     responses={
#         200: {"model": SuccessResponse[EventDetailSchema]},
#         400: {"model": ErrorResponse},
#         500: {"model": ErrorResponse}
#     }
# )
# async def delete_event_detail(
#     event_detail_id: uuid.UUID,
#     event_detail_delete_use_case: EventDetailDeleteUseCase = Depends(get_event_detail_delete_usecase)
# ):
#     try:
#         result = await event_detail_delete_use_case.call(event_detail_id)

#         return SuccessResponse(
#             status="success",
#             message=result["message"],
#             data={ "content": result["event"] },
#             status_code=200
#         )
#     except Exception as e:
#         print(e)
#         if "not found" in str(e):
#             raise HTTPException(status_code=404, detail={"error": str(e)})
#         else:
#             raise HTTPException(status_code=400, detail={"error": str(e)})
