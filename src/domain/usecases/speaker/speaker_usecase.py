import uuid
from src.domain.params.speaker.speaker_params import SpeakerParams
from src.infrastructure.database.models.speaker import SpeakerModel
from src.infrastructure.repositories.speaker.speaker_repository import SpeakerRepositoryImplementation
from src.utils.count_page import CountPage


class SpeakerUseCase:
    def __init__(
            self, 
            speaker_repos: SpeakerRepositoryImplementation
    ):
        self.speaker_repos = speaker_repos

    async def call_create(
            self, 
            params: SpeakerParams.Create
    ):
        try:
            created = await self.speaker_repos.create(
                name=params.name,
                title=params.title,
                social_media_links=params.social_media_links,
                company=params.company
            )
            return {
                "message": "Speaker created successfully", 
                "data": created.as_dict()
            }
        except Exception as e:
            return {"message": f"Error creating speaker: {str(e)}", "error": str(e)}

    async def call_update(
            self, 
            speaker_id: uuid.UUID | str,
            params: SpeakerParams.Update,
    ):
        try:
            current_speaker = await self.speaker_repos.find(speaker_id)

            if (current_speaker is None):
                raise Exception("Speaker tidak ditemukan")

            update_data = {}
            params_dict = vars(params)

            for field, new_value in params_dict.items():
                current_value = getattr(current_speaker, field)
                if new_value is not None and new_value != current_value:
                        update_data[field] = new_value

            if not update_data:
                return {"message": "No changes detected", "data": None}

            updated = await self.speaker_repos.update(
                speaker_id=speaker_id,
                **update_data
            )

            return {
                "message": "Speaker updated successfully", 
                "data": updated.as_dict()
            }
        except Exception as e:
            return {"message": f"Error updating speaker: {str(e)}", "error": str(e)}

    async def call_get(
            self, 
            params: SpeakerParams.Get
    ):
        try:
            if params.parameter is None:
                speaker = await self.speaker_repos.get_all(params.page, params.page_size)
                parsed_speakers = []
                for speaker in speaker:
                    parsed_speakers.append(speaker.as_dict())

                pages = await CountPage(
                        SpeakerModel, 
                        self.speaker_repos.db, 
                        params.page_size
                ).count()

                return {
                    "message": "Speakers retrieved successfully", 
                    "data": {
                        "speakers": parsed_speakers,
                        "current_page": params.page,
                        "page_size": params.page_size,
                        "pages": pages
                    }
                }

            speaker = await self.speaker_repos.get_by_name_or_title_or_company(params)
            parsed_speakers = []
            for speaker in speaker:
                parsed_speakers.append(speaker.as_dict())

            pages = await CountPage(
                    SpeakerModel, 
                    self.speaker_repos.db, 
                    params.page_size
            ).count_by("speaker_id", params.parameter)

            return {
                "message": "Speaker retrieved successfully", 
                "data": {
                    "speaker": parsed_speakers,
                    "current_page": params.page,
                    "page_size": params.page_size,
                    "pages": pages
                }
            }
        except Exception as e:
            print(f"Error retrieving speaker: {str(e)}")
            raise e

    async def call_find(
            self, 
            params: SpeakerParams.Find
    ):
        try:
            speaker = await self.speaker_repos.get_speaker(params.speaker_id)
            if speaker is None:
                raise Exception("Speaker not found")

            return {
                "message": "Speaker retrieved successfully", 
                "data": speaker.as_dict()
            }
        except Exception as e:
            print(f"Error retrieving speaker: {str(e)}")
            raise e

    async def call_delete(
            self, 
            params: SpeakerParams.Delete
    ):
        try:
            deleted = await self.speaker_repos.delete(params.speaker_id)
            return {
                "message": "Speaker deleted successfully", 
                "data": deleted.as_dict()
            }
        except Exception as e:
            return {"message": f"Error deleting speaker: {str(e)}", "error": str(e)}
