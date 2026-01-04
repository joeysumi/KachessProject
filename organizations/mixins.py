from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404

from organizations.models import Organization
from organizations.permissions import (
    user_is_org_admin,
    user_is_org_organizer,
    user_is_org_observer,
)

class OrganizationContextMixin:
    """
    Resolves the organization from the URL and attaches it to self.organization.

    Expects one of:
    - organization_pk
    - org_pk
    - organization_id
    """

    organization_url_kwarg = None  # optional override

    def get_organization(self):
        if self.organization_url_kwarg:
            kwarg = self.organization_url_kwarg
        else:
            kwarg = (
                "organization_pk"
                if "organization_pk" in self.kwargs
                else "org_pk"
                if "org_pk" in self.kwargs
                else "organization_id"
            )

        org_id = self.kwargs.get(kwarg)
        if org_id is None:
            raise RuntimeError("OrganizationContextMixin requires an organization URL kwarg")

        return get_object_or_404(Organization, pk=org_id)

    def dispatch(self, request, *args, **kwargs):
        self.organization = self.get_organization()
        return super().dispatch(request, *args, **kwargs)


class OrganizationAdminRequiredMixin(OrganizationContextMixin):
    """
    Allows access only to organization admins.
    """

    def dispatch(self, request, *args, **kwargs):
        self.organization = self.get_organization()

        if not user_is_org_admin(request.user, self.organization):
            raise PermissionDenied

        return super().dispatch(request, *args, **kwargs)


class OrganizationOrganizerRequiredMixin(OrganizationContextMixin):
    """
    Allows access to admins and organizers.
    """

    def dispatch(self, request, *args, **kwargs):
        self.organization = self.get_organization()

        if not user_is_org_organizer(request.user, self.organization):
            raise PermissionDenied

        return super().dispatch(request, *args, **kwargs)


class OrganizationObserverRequiredMixin(OrganizationContextMixin):
    """
    Allows access to any organization member (including observers).
    """

    def dispatch(self, request, *args, **kwargs):
        self.organization = self.get_organization()

        if not user_is_org_observer(request.user, self.organization) and not user_is_org_organizer(
            request.user, self.organization
        ):
            raise PermissionDenied

        return super().dispatch(request, *args, **kwargs)
