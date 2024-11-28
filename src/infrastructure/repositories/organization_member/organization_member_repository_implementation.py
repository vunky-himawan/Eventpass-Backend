from domain.repositories.organization_member.organization_member_repository import OrganizationMemberRepository
from sqlalchemy.ext.asyncio import AsyncSession
from infrastructure.database.models.organization_member import OrganizationMemberModel
from sqlalchemy import select

class OrganizationMemberRepositoryImplementation(OrganizationMemberRepository):
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def get_organization_member_by_user_id(self, user_id: int) -> dict:
        try:
            query = select(OrganizationMemberModel).where(OrganizationMemberModel.user_id == user_id)
            result = await self.db.execute(query)
            organization_member = result.scalars().first()

            if organization_member is None:
                raise ValueError("Organization member not found")

            return organization_member.to_dict()
        except ValueError as e:
            print(f"Error fetching organization member: {e}")
            raise e
        except Exception as e:
            print(f"Error fetching organization member: {e}")
            raise e