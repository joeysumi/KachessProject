from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404

from organizations.models import Organization
from organizations.permissions import (
    get_org_membership,
    has_org_capability,
)
from organizations.capabilities import OrgCapability


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


class OrganizationCapabilityRequiredMixin:
    """
    Base mixin for organization-scoped capability checks.

    Subclasses must define:
        required_capability: OrgCapability
    """

    required_capability = None

    def dispatch(self, request, *args, **kwargs):
        if self.required_capability is None:
            raise RuntimeError(
                "OrganizationCapabilityRequiredMixin requires "
                "`required_capability` to be set"
            )

        self.organization = self.get_organization()
        self.membership = get_org_membership(request.user, self.organization)

        if not has_org_capability(self.membership, self.required_capability):
            raise PermissionDenied

        return super().dispatch(request, *args, **kwargs)


class OrganizationReadRequiredMixin(
    OrganizationContextMixin,
    OrganizationCapabilityRequiredMixin,
):
    required_capability = OrgCapability.READ


class OrganizationWriteRequiredMixin(
    OrganizationContextMixin,
    OrganizationCapabilityRequiredMixin,
):
    required_capability = OrgCapability.WRITE


class OrganizationDeleteRequiredMixin(
    OrganizationContextMixin,
    OrganizationCapabilityRequiredMixin,
):
    required_capability = OrgCapability.DELETE
