from abc import ABC, abstractmethod

class OrganizationMemberRepository(ABC):
    @abstractmethod
    async def get_organization_member_by_user_id(self, user_id: int) -> dict:
        pass