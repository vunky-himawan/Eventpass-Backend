import uuid
from src.domain.params.organizer.event_organizer_params import EventOrganizerParams
from src.infrastructure.database.models.event_organizer import EventOrganizerModel
from src.infrastructure.database.models.user import RoleEnum, UserModel
from src.infrastructure.repositories.organizer.event_organizer_repo_implements import EventOrganizerRepositoryImplementation
from src.utils.count_page import CountPage


class EventOrganizerUseCase:
    def __init__(
        self, 
        event_organizer_repos: EventOrganizerRepositoryImplementation,
    ):
        self.event_organizer_repos = event_organizer_repos

    async def call_create(
        self, 
        params: EventOrganizerParams.Create
    ):
        try:
            event_organizer = await self.event_organizer_repos.create(params)
            if event_organizer:
                user = await self.event_organizer_repos.db.get(UserModel, event_organizer.user_id)

                if user:
                    user.role = RoleEnum.EVENT_ORGANIZER.value
                    await self.event_organizer_repos.db.commit()
                else:
                    raise Exception("User not found")

            return {
                "message": "Event organizer created successfully",
                "data": event_organizer.as_dict()
            }
        except Exception as e:
            print(f"Error creating event organizer: {str(e)}")
            await self.event_organizer_repos.db.rollback()
            raise e

    async def call_update(
        self, 
        event_organizer_id: str | uuid.UUID,
        params: EventOrganizerParams.Update
    ):
        try:
            org_id = event_organizer_id if isinstance(event_organizer_id, str) else event_organizer_id

            current_event_organizer = await self.event_organizer_repos.find(EventOrganizerParams.Find(organizer_id=org_id))
            
            if params.user_id:
                user = await self.event_organizer_repos.db.get(UserModel, params.user_id)
                old_user = await self.event_organizer_repos.db.get(UserModel, current_event_organizer.user_id)

                if user:
                    user.role = RoleEnum.EVENT_ORGANIZER.value
                    if old_user:
                        old_user.role = RoleEnum.PARTICIPANT.value

                    await self.event_organizer_repos.db.commit()
                else:
                    raise Exception("User not found")

            if (current_event_organizer is None):
                raise Exception("Event organizer tidak ditemukan")

            update_data = {}
            params_dict = vars(params)

            for field, new_value in params_dict.items():
                current_value = getattr(current_event_organizer, field)
                if new_value is not None and new_value != current_value:
                        update_data[field] = new_value

            if not update_data:
                return {"message": "No changes detected", "data": None}

            event_organizer = await self.event_organizer_repos.update(event_organizer_id, **update_data)
            return {
                "message": "Event organizer updated successfully",
                "data": event_organizer.as_dict()
            }
        except Exception as e:
            print(f"Error updating event organizer: {str(e)}")            
            await self.event_organizer_repos.db.rollback()
            raise e

    async def call_delete(
        self, 
        params: EventOrganizerParams.Delete
    ):
        try:
            event_organizer = await self.event_organizer_repos.delete(params)
            return {
                "message": "Event organizer deleted successfully",
                "data": event_organizer.as_dict()
            }
        except Exception as e:
            return {"message": f"Error deleting event organizer: {str(e)}", "error": str(e)}

    async def call_get(
        self, 
        params: EventOrganizerParams.Get
    ):
        try:
            if not params.parameter:
                organizers = await self.event_organizer_repos.get_all(params)
                prepared_organizers = [await organizer.as_dict_with_relations() for organizer in organizers]
                pages = await CountPage(EventOrganizerModel, self.event_organizer_repos.db, params.page_size).count()

                return {
                    "message": "Event organizers retrieved successfully",
                    "data": {
                        "organizers": prepared_organizers,
                        "current_page": params.page,
                        "page_size": params.page_size,
                        "pages": pages,
                    }
                }

            organizer = await self.event_organizer_repos.get_by_name_or_email(params)
            prepared_organizer = [await organizer.as_dict_with_relations() for organizer in organizer]
            pages = await CountPage(EventOrganizerModel, self.event_organizer_repos.db, params.page_size).count_by("organization_name", params.parameter)

            return {
                "message": "Event organizer retrieved successfully",
                "data": {
                    "organizer": prepared_organizer,
                    "current_page": params.page,
                    "page_size": params.page_size,
                    "pages": pages,
                }
            }
        
        except Exception as e:
            print(f"Error retrieving event organizer: {str(e)}")
            raise e

    async def call_find(
        self, 
        params: EventOrganizerParams.Find
    ): 
        try:
            organizer = await self.event_organizer_repos.find(params)
            prepared_organizer = await organizer.as_dict_with_relations()

            return {
                "message": "Event organizer retrieved successfully",
                "data": prepared_organizer
            }
        except Exception as e:
            print(f"Error retrieving event organizer: {str(e)}")
            raise e
