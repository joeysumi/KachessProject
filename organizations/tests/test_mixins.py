from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied
from django.test import RequestFactory, TestCase
from django.views.generic import TemplateView

from organizations.mixins import (
    OrganizationObserverRequiredMixin,
    OrganizationOrganizerRequiredMixin,
    OrganizationAdminRequiredMixin,
)
from organizations.models import Organization, OrganizationMembership

User = get_user_model()


class OrganizationMixinTestBase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

        self.org = Organization.objects.create(name="Test Org")

        self.admin = User.objects.create_user(
            username="admin",
            email="admin@test.com",
            password="pw",
        )

        self.organizer = User.objects.create_user(
            username="organizer",
            email="org@test.com",
            password="pw",
        )

        self.observer = User.objects.create_user(
            username="observer",
            email="obs@test.com",
            password="pw",
        )

        OrganizationMembership.objects.create(
            user=self.admin,
            organization=self.org,
            role=OrganizationMembership.Role.ADMIN,
        )

        OrganizationMembership.objects.create(
            user=self.organizer,
            organization=self.org,
            role=OrganizationMembership.Role.ORGANIZER,
        )

        OrganizationMembership.objects.create(
            user=self.observer,
            organization=self.org,
            role=OrganizationMembership.Role.OBSERVER,
        )

class ObserverView(OrganizationObserverRequiredMixin, TemplateView):
    template_name = "dummy.html"


class OrganizerView(OrganizationOrganizerRequiredMixin, TemplateView):
    template_name = "dummy.html"


class AdminView(OrganizationAdminRequiredMixin, TemplateView):
    template_name = "dummy.html"

def dispatch(view_cls, user, org):
    request = RequestFactory().get("/")
    request.user = user

    return view_cls.as_view()(request, organization_id=org.id)


class TestOrganizationObserverRequiredMixin(OrganizationMixinTestBase):

    def test_member_is_allowed(self):
        response = dispatch(ObserverView, self.observer, self.org)
        self.assertEqual(response.status_code, 200)

    def test_non_member_is_denied(self):
        outsider = User.objects.create_user(
            username="outsider",
            email="out@test.com",
            password="pw",
        )

        with self.assertRaises(PermissionDenied):
            dispatch(ObserverView, outsider, self.org)


class TestOrganizationOrganizerRequiredMixin(OrganizationMixinTestBase):

    def test_admin_is_allowed(self):
        response = dispatch(OrganizerView, self.admin, self.org)
        self.assertEqual(response.status_code, 200)

    def test_organizer_is_allowed(self):
        response = dispatch(OrganizerView, self.organizer, self.org)
        self.assertEqual(response.status_code, 200)

    def test_observer_is_denied(self):
        with self.assertRaises(PermissionDenied):
            dispatch(OrganizerView, self.observer, self.org)


class TestOrganizationAdminRequiredMixin(OrganizationMixinTestBase):

    def test_admin_is_allowed(self):
        response = dispatch(AdminView, self.admin, self.org)
        self.assertEqual(response.status_code, 200)

    def test_organizer_is_denied(self):
        with self.assertRaises(PermissionDenied):
            dispatch(AdminView, self.organizer, self.org)

    def test_observer_is_denied(self):
        with self.assertRaises(PermissionDenied):
            dispatch(AdminView, self.observer, self.org)
