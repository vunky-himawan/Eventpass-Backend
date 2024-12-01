from typing import Sequence
import uuid
from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from src.domain.params.organizer.event_organizer_params import EventOrganizerParams
from src.domain.repositories.organizer.event_organizer_repo import EventOrganizerRepository
from src.infrastructure.database.models.event_organizer import EventOrganizerModel


class EventOrganizerRepositoryImplementation(EventOrganizerRepository):
    def __init__(
            self, 
            db: AsyncSession
    ):
        self.db = db

    async def get_event_organizer(self, event_organizer_id: str | uuid.UUID) -> EventOrganizerModel:
        try:
            if isinstance(event_organizer_id, str):
                event_organizer_id = uuid.UUID(event_organizer_id)

            event_organizer = await self.db.get(EventOrganizerModel, event_organizer_id)
            return event_organizer
        except Exception as e:
            print(f"Error fetching event organizer: {e}")
            raise e

    async def create(self, params: EventOrganizerParams.Create) -> EventOrganizerModel:
        try:
            event_organizer = EventOrganizerModel(
                user_id=params.user_id,
                organization_name=params.organization_name,
                address=params.address,
                phone_number=params.phone_number,
                email=params.email,
                description=params.description,
                amount=params.amount,
            )
            self.db.add(event_organizer)
            await self.db.commit()
            await self.db.refresh(event_organizer)
            return event_organizer
        except Exception as e:
            print(f"Error creating event organizer: {e}")
            raise e
    
    async def update(self, event_organizer_id: str | uuid.UUID, **update_data: EventOrganizerParams.Update) -> EventOrganizerModel:
        try:
            event_organizer = await self.db.get(EventOrganizerModel, event_organizer_id)
            if not event_organizer:
                raise Exception("Event organizer not found")

            for key, value in update_data.items():
                setattr(event_organizer, key, value)

            await self.db.commit()
            await self.db.refresh(event_organizer)
            return event_organizer
        except Exception as e:
            print(f"Error updating event organizer: {e}")
            await self.db.rollback()
            raise e

    async def delete(self, params: EventOrganizerParams.Delete) -> EventOrganizerModel:
        try:
            event_organizer = await self.db.get(EventOrganizerModel, params.event_organizer_id)
            if not event_organizer:
                raise Exception("Event organizer not found")

            await self.db.delete(event_organizer)
            await self.db.commit()

            return event_organizer
        except Exception as e:
            print(f"Error deleting event organizer: {e}")
            await self.db.rollback()
            raise e

    async def get_all(self, params: EventOrganizerParams.Get) -> Sequence[EventOrganizerModel]:
        try:
            query = select(EventOrganizerModel).order_by(
                EventOrganizerModel.created_at.desc()
            ).limit(
                params.page_size
            ).offset((params.page - 1) * params.page_size)

            event_organizers = await self.db.execute(query)
            return event_organizers.scalars().all()
        except Exception as e:
            print(f"Error fetching event organizers: {e}")
            raise e

    async def find(self, params: EventOrganizerParams.Find) -> EventOrganizerModel:
        try:
            event_organizers = await self.db.get(EventOrganizerModel, params.organizer_id)
            return event_organizers
        except Exception as e:
            print(f"Error fetching event organizers: {e}")
            raise e

    async def get_by_name_or_email(self, params: EventOrganizerParams.Get) -> Sequence[EventOrganizerModel]:
        try:
            query = select(EventOrganizerModel).where(
                    or_(
                        EventOrganizerModel.user_id.ilike(f"%{params.parameter}%"),
                        EventOrganizerModel.organization_name.ilike(f"%{params.parameter}%"),
                        EventOrganizerModel.email.ilike(f"%{params.parameter}%")
                    )
                )

            event_organizers = await self.db.execute(query)
            return event_organizers.scalars().all()
        except Exception as e:
            print(f"Error fetching event organizers: {e}")
            raise e
