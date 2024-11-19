
import uuid
from domain.params.event.detail.main import EventDetailCreationParams, EventDetailUpdateParams
from infrastructure.repositories.event.detail.main import EventDetailRepositoryImplementation
from infrastructure.repositories.event.main import EventRepositoryImplementation


class EventDetailCreationUseCase:
    def __init__(
            self, 
            event_detail_repository: EventDetailRepositoryImplementation,
            event_repository: EventRepositoryImplementation,
            # employee_repository: EmployeeRepositoryImplementation
        ):
        self.event_detail_repository = event_detail_repository
        self.event_repository = event_repository

    async def call(self, event_id: uuid.UUID, params: EventDetailCreationParams):
        try:
            eventExist = await self.event_repository.get_event(event_id)
            if not eventExist:
                raise Exception("Event not found")

            event_detail = await self.event_detail_repository.create_event_detail(
                event_id=event_id,
                event_receiptionist_id=params.event_receiptionist_id,
                speaker_id=params.speaker_id
            )

            return {"message": "Event created successfully", "event": event_detail.as_dict()}
        except Exception as e:
            print(f"Error creating event detail: {e}")
            raise Exception(f"Error creating event detail: {e}")

class EventDetailUpdateUseCase:
    def __init__(self, event_detail_repository: EventDetailRepositoryImplementation):
        self.event_detail_repository = event_detail_repository

    async def call(self, event_detail_id: uuid.UUID, params: EventDetailUpdateParams):
        try:
            isExist = await self.event_detail_repository.get_event_detail(event_detail_id=event_detail_id)
            if not isExist:
                raise Exception("Event not found")

            update_data = {}
            params_dict = vars(params)

            for field, new_value in params_dict.items():
                current_value = getattr(isExist, field)
                if new_value is not None and new_value != current_value:
                    update_data[field] = new_value

            # If there are any changes, update the event
            if update_data:
                new_event_detail = await self.event_detail_repository.update_event_detail(
                    event_detail_id=event_detail_id,
                    **update_data
                )
    
                return {"message": "Event updated successfully", "event": new_event_detail.as_dict()}

            else:
                return {"message": "No changes detected"}

        except Exception as e:
            raise Exception(f"Error updating event detail: {e}")


class EventDetailDeleteUseCase:
    def __init__(self, event_detail_repository: EventDetailRepositoryImplementation):
        self.event_detail_repository = event_detail_repository

    async def call(self, event_detail_id: uuid.UUID):
        try:
            isExist = await self.event_detail_repository.get_event_detail(event_detail_id=event_detail_id)
            if not isExist:
                raise Exception("Event not found")

            # Delete the event from the database
            await self.event_detail_repository.delete_event_detail(event_detail_id)

            return {"message": "Event deleted successfully", "event": f"ID: {event_detail_id} || Title: {isExist.title}"}

        except Exception as e:
            raise Exception(f"Error deleting event detail: {e}")
