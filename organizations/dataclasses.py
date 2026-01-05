from dataclasses import dataclass
from organizations.models import OrganizationMembership


@dataclass(frozen=True)
class OrgMembershipView:
    role: OrganizationMembership.Role
