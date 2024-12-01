import uuid
from domain.entities.result.result import Failed
from domain.params.event.main import EventCreationParams, UpdateEventParams
from infrastructure.repositories.event.main import EventRepositoryImplementation
from infrastructure.services.image_service import ImageService
from src.infrastructure.database.models.event import EventModel
from src.infrastructure.repositories.event_speaker.event_speaker_repos import EventSpeakerRepositoryImplementation
from src.infrastructure.repositories.speaker.speaker_repository import SpeakerRepositoryImplementation
from src.utils.count_page import CountPage


class EventCreationUseCase:
    def __init__(
            self, 
            image_service: ImageService, 
            event_repository: EventRepositoryImplementation,
            speaker_repos: SpeakerRepositoryImplementation,
            event_speaker_repos: EventSpeakerRepositoryImplementation,
    ):
        self.image_service = image_service
        self.event_repository = event_repository
        self.speaker_repos = speaker_repos
        self.event_speaker_repos = event_speaker_repos

    async def call(self, params: EventCreationParams):
        try:
            filename = f"{uuid.uuid4().hex}_{params.thumbnail.filename}"
            thumbnail_path = self.image_service.save_image(
                        params.thumbnail, 
                        filename, 
                        subdir=f"{uuid.uuid4()}-{params.title}"
                        )

            new_event = await self.event_repository.create_event(
                title=params.title,
                thumbnail_path=thumbnail_path,
                address=params.address,
                description=params.description,
                type=params.type,
                status=params.status,
                ticket_price=params.ticket_price,
                ticket_quantity=params.ticket_quantity,
                start_date=params.start_date.strftime("%Y-%m-%d %H:%M:%S"),
                event_organizer_id=params.event_organizer_id,
                receptionist_1=params.receptionist_1,
                receptionist_2=params.receptionist_2,
            )

            speakers = params.speaker
            new_speakers = []
            if speakers and len(speakers) > 0:
                for speaker in speakers:
                    created = await self.speaker_repos.create(
                            name=speaker.name,
                            title=speaker.title,
                            social_media_links=speaker.social_media_links,
                            company=speaker.company
                    )
                    new_speakers.append(created.as_dict())

            new_event_speakers = []
            if new_speakers and len(speakers) > 0:
                for speaker in new_speakers:
                    created_event_speaker = await self.event_speaker_repos.create(
                            event_id=new_event.event_id,
                            speaker_id=speaker["speaker_id"]
                    )
                    new_event_speakers.append(created_event_speaker.as_dict())

            combined_data = {
                "event": new_event.as_dict(),
            }

            if new_event_speakers:
                combined_data["event"]["event_speakers"] = new_event_speakers

            if new_speakers:
                for combined_speaker in combined_data["event"]["event_speakers"]:
                    for speaker in new_speakers:
                        if combined_speaker["speaker_id"] == speaker["speaker_id"]:
                            combined_speaker["speaker"] = speaker

            return {
                "message": "Event created successfully", 
                "data": combined_data
            }
        except Exception as e:
            return {"message": f"Error creating event: {str(e)}", "error": str(e)}

class EventUpdateUseCase:
    def __init__(
            self, 
            image_service: ImageService, 
            event_repository: EventRepositoryImplementation,
            speaker_repos: SpeakerRepositoryImplementation,
            event_speaker_repos: EventSpeakerRepositoryImplementation,
        ):
        self.image_service = image_service
        self.event_repository = event_repository
        self.speaker_repos = speaker_repos
        self.event_speaker_repos = event_speaker_repos

    async def call(self, event_id: uuid.UUID, params: UpdateEventParams):
        try:
            current_event = await self.event_repository.get_event(event_id)

            if (current_event is None):
                raise Exception("Event tidak ditemukan")

            update_data = {}

            params_dict = vars(params)

            for field, new_value in params_dict.items():
                if field == "thumbnail" or field == "speaker" or new_value is None:
                    continue

                current_value = getattr(current_event, field)
                if new_value is not None and new_value != current_value:
                    if field == "status" or field == "type":
                        update_data[field] = new_value.name
                    else:
                        update_data[field] = new_value

            if params.thumbnail:
                filename = f"{uuid.uuid4().hex}_{params.thumbnail.filename}"
                thumbnail_path = self.image_service.save_image(
                    params.thumbnail,
                    filename,
                    subdir=f"{uuid.uuid4()}-{params.title}"
                )
                update_data["thumbnail_path"] = thumbnail_path
            
            if update_data:
                new_event = await self.event_repository.update_event(
                    event_id=event_id,
                    **update_data
                )

            new_event = await self.event_repository.get_event(event_id)

            speakers = params.speaker
            if speakers and len(speakers) > 0:
                updated_event_speakers = []
                for speaker in speakers:
                    updated_event_speaker = await self.event_speaker_repos.update(
                        event_speaker_id=speaker.event_speaker_id,
                        event_id=speaker.event_id,
                        speaker_id=speaker.speaker_id
                    )
                    updated_event_speakers.append(updated_event_speaker.as_dict())

                if not updated_event_speakers:
                    return {"message": "No changes detected", "data": None}
                
                with_relations = await current_event.as_dict_with_relations()

                combined_data = {
                    "event": with_relations,
                }

                return {
                    "message": "Event updated successfully", 
                    "data": combined_data
                }

            else:
                return {"message": "No changes detected", "data": None}

        except Exception as e:
            print(f"Error updating event: {str(e)}")
            raise e

class EventDeleteUseCase:
    def __init__(
        self, 
        event_repository: EventRepositoryImplementation
    ):
        self.event_repository = event_repository

    async def call(self, event_id: uuid.UUID):
        try:
            current_event = await self.event_repository.get_event(event_id)

            if (current_event is None):
                raise Exception("Event tidak ditemukan")

            await self.event_repository.delete_event(event_id)

            return {"message": "Event deleted successfully", "event": f"ID: {event_id} || Title: {current_event.title}"}
        except Exception as e:
            return {"message": f"Error deleting event: {str(e)}", "error": str(e)}


class EventGetUseCase:
    def __init__(
            self, 
            event_repository: EventRepositoryImplementation
    ):
        self.event_repository = event_repository

    async def call(
            self, 
            current_page: int = 1, 
            page_size: int = 10
    ):
        try:
            events = await self.event_repository.get_all(current_page, page_size)
            serialized_events = [await event.as_dict_with_relations() for event in events]

            # count = await self.event_repository.get_count_all()
            # pages = 1
            # if count and count > 1:
            #     pages = (count + page_size - 1) // page_size if count > 0 else 1
            pages = await CountPage(EventModel, self.event_repository.db, page_size).count()

            return {
                    "message": "Events retrieved successfully", 
                    "data": {
                        "events": serialized_events,
                        "current_page": current_page,
                        "page_size": page_size,
                        "pages": pages,
                    }
             }
        except Exception as e:
            print(f"Error retrieving events: {str(e)}")
            return {"message": f"Error retrieving events: {str(e)}", "error": str(e)}

    async def call_one(self, event_id: uuid.UUID):
        try:
            current_event = await self.event_repository.get_event(event_id)

            if (current_event is None):
                raise Exception("Event tidak ditemukan")

            return {
                    "message": "Event retrieved successfully", 
                    "data": await current_event.as_dict_with_relations()
             }
        except Exception as e:
            print(f"Error retrieving events: {str(e)}")
            raise e

    async def call_by_title_or_type(
            self, 
            params: str,
            current_page: int = 1,
            page_size: int = 10
    ):
        try:
            events = await self.event_repository.get_all_by_title_or_type_or_status(params)
            serialized_events = [await event.as_dict_with_relations() for event in events]

            count = await CountPage(EventModel, self.event_repository.db, page_size).count_by("title", params)

            return {
                    "message": "Events retrieved successfully", 
                    "data": {
                        "events": serialized_events,
                        "current_page": current_page,
                        "page_size": page_size,
                        "pages": count,
                    }
             }
        except Exception as e:
            print(f"Error retrieving events: {str(e)}")
            raise e
