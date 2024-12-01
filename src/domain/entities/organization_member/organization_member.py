from dataclasses import dataclass

@dataclass
class OrganizationMember:
    organization_member_id: str
    user_id: str
    event_organizer_id: str