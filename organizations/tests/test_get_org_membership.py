from django.contrib.auth import get_user_model
from django.test import TestCase, override_settings

from organizations.models import OrganizationMembership
from organizations.permissions import get_org_membership
from organizations.tests.factories import (
    UserFactory,
    OrganizationFactory,
    OrganizationMembershipFactory,
)

User = get_user_model()


@override_settings(ROOT_URLCONF="organizations.tests.urls")
class TestGetOrgMembership(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.org = OrganizationFactory()

        cls.admin = UserFactory()
        cls.outsider = UserFactory()

        cls.membership = OrganizationMembershipFactory(
            user=cls.admin,
            organization=cls.org,
            role=OrganizationMembership.Role.ADMIN,
        )

    def test_returns_membership_for_member(self):
        membership = get_org_membership(self.admin, self.org)
        self.assertEqual(membership, self.membership)

    def test_returns_none_for_non_member(self):
        self.assertIsNone(get_org_membership(self.outsider, self.org))

    def test_returns_none_for_anonymous(self):
        self.assertIsNone(get_org_membership(None, self.org))
