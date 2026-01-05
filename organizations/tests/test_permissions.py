from django.test import SimpleTestCase

from organizations.dataclasses import OrgMembershipView
from organizations.models import OrganizationMembership
from organizations.permissions import (
    can_read_in_organization,
    can_write_in_organization,
    can_delete_in_organization,
)


class TestOrganizationPermissions(SimpleTestCase):

    def test_admin_capabilities__can_read_write_delete(self):
        membership = OrgMembershipView(role=OrganizationMembership.Role.ADMIN)

        self.assertTrue(can_read_in_organization(membership))
        self.assertTrue(can_write_in_organization(membership))
        self.assertTrue(can_delete_in_organization(membership))

    def test_organizer_capabilities__can_read_write(self):
        membership = OrgMembershipView(role=OrganizationMembership.Role.ORGANIZER)

        self.assertTrue(can_read_in_organization(membership))
        self.assertTrue(can_write_in_organization(membership))
        self.assertFalse(can_delete_in_organization(membership))

    def test_observer_capabilities__can_read(self):
        membership = OrgMembershipView(role=OrganizationMembership.Role.OBSERVER)

        self.assertTrue(can_read_in_organization(membership))
        self.assertFalse(can_write_in_organization(membership))
        self.assertFalse(can_delete_in_organization(membership))

    def test_non_member__has_no_capabilities(self):
        self.assertFalse(can_read_in_organization(None))
        self.assertFalse(can_write_in_organization(None))
        self.assertFalse(can_delete_in_organization(None))
