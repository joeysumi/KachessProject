from django.contrib.auth import get_user_model
from django.test import TestCase

from organizations.models import (
    Organization,
    OrganizationMembership,
)
from organizations.permissions import (
    get_org_membership,
    user_is_org_admin,
    user_is_org_organizer,
    user_is_org_observer,
)

User = get_user_model()


class TestOrganizationPermission(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.org = Organization.objects.create(name="Test Org")

        cls.admin = User.objects.create(
            username="admin",
            email="admin@example.com",
        )

        cls.organizer = User.objects.create(
            username="organizer",
            email="organizer@example.com",
        )

        cls.observer = User.objects.create(
            username="observer",
            email="observer@example.com",
        )

        cls.outsider = User.objects.create(
            username="outsider",
            email="outsider@example.com",
        )

        OrganizationMembership.objects.create(
            user=cls.admin,
            organization=cls.org,
            role=OrganizationMembership.Role.ADMIN,
        )

        OrganizationMembership.objects.create(
            user=cls.organizer,
            organization=cls.org,
            role=OrganizationMembership.Role.ORGANIZER,
        )

        OrganizationMembership.objects.create(
            user=cls.observer,
            organization=cls.org,
            role=OrganizationMembership.Role.OBSERVER,
        )

    def test_get_org_membership_returns_membership(self):
        membership = get_org_membership(self.admin, self.org)
        self.assertIsNotNone(membership)
        self.assertEqual(membership.role, OrganizationMembership.Role.ADMIN)

    def test_get_org_membership_returns_none_for_non_member(self):
        membership = get_org_membership(self.outsider, self.org)
        self.assertIsNone(membership)

    def test_get_org_membership_fails_closed_for_anonymous(self):
        membership = get_org_membership(None, self.org)
        self.assertIsNone(membership)

    def test_user_is_org_admin(self):
        self.assertTrue(user_is_org_admin(self.admin, self.org))

    def test_organizer_is_not_admin(self):
        self.assertFalse(user_is_org_admin(self.organizer, self.org))

    def test_observer_is_not_admin(self):
        self.assertFalse(user_is_org_admin(self.observer, self.org))

    def test_non_member_is_not_admin(self):
        self.assertFalse(user_is_org_admin(self.outsider, self.org))

    def test_admin_is_organizer(self):
        self.assertTrue(user_is_org_organizer(self.admin, self.org))

    def test_organizer_is_organizer(self):
        self.assertTrue(user_is_org_organizer(self.organizer, self.org))

    def test_observer_is_not_organizer(self):
        self.assertFalse(user_is_org_organizer(self.observer, self.org))

    def test_non_member_is_not_organizer(self):
        self.assertFalse(user_is_org_organizer(self.outsider, self.org))

    def test_observer_is_observer(self):
        self.assertTrue(user_is_org_observer(self.observer, self.org))

    def test_admin_is_not_observer(self):
        self.assertFalse(user_is_org_observer(self.admin, self.org))

    def test_organizer_is_not_observer(self):
        self.assertFalse(user_is_org_observer(self.organizer, self.org))

    def test_non_member_is_not_observer(self):
        self.assertFalse(user_is_org_observer(self.outsider, self.org))
