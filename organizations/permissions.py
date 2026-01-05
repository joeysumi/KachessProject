from typing import Optional, Protocol
from django.contrib.auth import get_user_model

from organizations.models import Organization, OrganizationMembership
from organizations.capabilities import OrgCapability

User = get_user_model()

class HasOrgRole(Protocol):
    role: str

# --------------------
# DB boundary
# --------------------

def get_org_membership(
    user: User,
    organization: Organization,
) -> Optional[OrganizationMembership]:
    """
    Canonical way to fetch a user's membership in an organization.

    Returns:
        OrganizationMembership if it exists, otherwise None.
    """
    if user is None or not user.is_authenticated:
        return None

    return (
        OrganizationMembership.objects
        .filter(user=user, organization=organization)
        .first()
    )

# --------------------
# Pure permission logic
# --------------------

ORG_ROLE_CAPABILITIES = {
    OrganizationMembership.Role.ADMIN: {
        OrgCapability.READ,
        OrgCapability.WRITE,
        OrgCapability.DELETE,
    },
    OrganizationMembership.Role.ORGANIZER: {
        OrgCapability.READ,
        OrgCapability.WRITE,
    },
    OrganizationMembership.Role.OBSERVER: {
        OrgCapability.READ,
    },
}

def has_org_capability(
    membership: Optional[HasOrgRole],
    capability: OrgCapability,
) -> bool:
    """
    Returns True if the given membership grants the specified capability.
    Fails closed for None or unknown roles.
    """
    if membership is None:
        return False

    return capability in ORG_ROLE_CAPABILITIES.get(
        membership.role,
        set(),
    )

# --------------------
# Human-facing helpers
# --------------------

def can_read_in_organization(
    membership: Optional[OrganizationMembership],
) -> bool:
    return has_org_capability(membership, OrgCapability.READ)

def can_write_in_organization(
    membership: Optional[OrganizationMembership],
) -> bool:
    return has_org_capability(membership, OrgCapability.WRITE)

def can_delete_in_organization(
    membership: Optional[OrganizationMembership],
) -> bool:
    return has_org_capability(membership, OrgCapability.DELETE)
