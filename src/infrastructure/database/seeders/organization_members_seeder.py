from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from infrastructure.database.models.user import UserModel
from infrastructure.database.models.organization_member import OrganizationMemberModel
from infrastructure.database.models.event_organizer import EventOrganizerModel
from sqlalchemy.orm import selectinload

async def organization_members_seeder(db: AsyncSession):
    try:
        query = select(UserModel).where(UserModel.role == "RECEPTIONIST")
        result = await db.execute(query)
        receptionist = result.scalars().first()

        query = select(UserModel).where(UserModel.role == "EVENT_ORGANIZER").join(EventOrganizerModel, UserModel.user_id == EventOrganizerModel.user_id).options(selectinload(UserModel.event_organizer))
        result = await db.execute(query)
        user = result.scalars().first()
        event_organizer = user.event_organizer

        new_organization_member = OrganizationMemberModel(
            user_id=receptionist.user_id,
            event_organizer_id=event_organizer.event_organizer_id
        )

        db.add(new_organization_member)
        await db.commit()
        await db.refresh(new_organization_member)

    except Exception as e:
        await db.rollback()
        print(f"Error seeding organization members: {e}")