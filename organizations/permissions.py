from typing import Optional
from django.contrib.auth import get_user_model
from organizations.models import Organization, OrganizationMembership

User = get_user_model()

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

def user_is_org_admin(user: User, organization: Organization) -> bool:
    """
    True only if the user is an ADMIN of the organization.
    """
    membership = get_org_membership(user, organization)
    if membership is None:
        return False

    return membership.role == OrganizationMembership.Role.ADMIN

def user_is_org_organizer(user: User, organization: Organization) -> bool:
    """
    True if the user has WRITE access at the organization level.

    ADMIN → True
    ORGANIZER → True
    OBSERVER → False
    """
    membership = get_org_membership(user, organization)
    if membership is None:
        return False

    return membership.role in {
        OrganizationMembership.Role.ADMIN,
        OrganizationMembership.Role.ORGANIZER,
    }

def user_is_org_observer(user: User, organization: Organization) -> bool:
    """
    True if the user is an OBSERVER in the organization.
    """
    membership = get_org_membership(user, organization)
    if membership is None:
        return False

    return membership.role == OrganizationMembership.Role.OBSERVER
