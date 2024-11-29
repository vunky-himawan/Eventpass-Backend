import uuid
from domain.entities.result.result import Failed
from domain.params.event.main import EventCreationParams, UpdateEventParams
from infrastructure.repositories.event.main import EventRepositoryImplementation
from infrastructure.services.image_service import ImageService
from src.infrastructure.repositories.event_speaker.event_speaker_repos import EventSpeakerRepositoryImplementation
from src.infrastructure.repositories.speaker.speaker_repository import SpeakerRepositoryImplementation


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
            # Fetch the current event from the database
            current_event = await self.event_repository.get_event(event_id)

            if (current_event is None):
                raise Exception("Event tidak ditemukan")

            # Initialize update_data as a dictionary to track changes
            update_data = {}

            # Prepare the parameters dynamically
            params_dict = vars(params)  # Converts params to a dictionary

            # Compare and collect changed fields
            for field, new_value in params_dict.items():
                if field == "thumbnail" or new_value is None:
                    continue

                current_value = getattr(current_event, field)
                if new_value is not None and new_value != current_value:
                    update_data[field] = new_value

            # Handle the thumbnail separately if provided
            if params.thumbnail:
                filename = f"{uuid.uuid4().hex}_{params.thumbnail.filename}"
                thumbnail_path = self.image_service.save_image(
                    params.thumbnail,
                    filename,
                    subdir=f"{uuid.uuid4()}-{params.title}"
                )
                update_data["thumbnail_path"] = thumbnail_path

            # If there are any changes, update the event
            if update_data:
                new_event = await self.event_repository.update_event(
                    event_id=event_id,
                    **update_data
                )

                speakers = params.speaker
                updated_speakers = []
                if speakers:
                    for speaker in speakers:
                        updated = await self.speaker_repos.update(speaker.speaker_id, **speaker.dict())
                        updated_speakers = updated.__dict__
                        updated_speakers.append(updated)


                return {"message": "Event updated successfully", "event": new_event.as_dict()}
            else:
                return {"message": "No changes detected"}

        except Exception as e:
            return {"message": f"Error updating event: {str(e)}", "error": str(e)}

class EventDeleteUseCase:
    def __init__(self, event_repository):
        self.event_repository = event_repository

    async def call(self, event_id: uuid.UUID):
        try:
            # Fetch the current event from the database
            current_event = await self.event_repository.get_event(event_id)

            if (current_event is None):
                raise Exception("Event tidak ditemukan")

            # Delete the event from the database
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

    async def call(self):
        try:
            events = await self.event_repository.get_all()
            serialized_events = [event.as_dict() for event in events]

            return {"message": "Events retrieved successfully", "events": serialized_events}
        except Exception as e:
            print(f"Error retrieving events: {str(e)}")
            return {"message": f"Error retrieving events: {str(e)}", "error": str(e)}
