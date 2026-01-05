from django.test import TestCase, override_settings
from django.urls import reverse

from organizations.models import OrganizationMembership
from organizations.tests.factories import (
    OrganizationFactory,
    OrganizationMembershipFactory,
    UserFactory
)


@override_settings(ROOT_URLCONF="organizations.tests.urls")
class OrganizationMixinTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.org = OrganizationFactory()

        cls.admin = UserFactory()
        cls.organizer = UserFactory()
        cls.observer = UserFactory()
        cls.outsider = UserFactory()

        OrganizationMembershipFactory(
            user=cls.admin,
            organization=cls.org,
            role=OrganizationMembership.Role.ADMIN,
        )

        OrganizationMembershipFactory(
            user=cls.organizer,
            organization=cls.org,
            role=OrganizationMembership.Role.ORGANIZER,
        )

        OrganizationMembershipFactory(
            user=cls.observer,
            organization=cls.org,
            role=OrganizationMembership.Role.OBSERVER,
        )

    def test_read_allows_any_member(self):
        for user in (self.admin, self.organizer, self.observer):
            self.client.force_login(user)
            response = self.client.get(
                reverse("org-read", args=[self.org.pk])
            )
            self.assertEqual(response.status_code, 200)

    def test_read_denies_non_member(self):
        self.client.force_login(self.outsider)
        response = self.client.get(
            reverse("org-read", args=[self.org.pk])
        )
        self.assertEqual(response.status_code, 403)

    def test_write_allows_admin_and_organizer(self):
        for user in (self.admin, self.organizer):
            self.client.force_login(user)
            response = self.client.post(
                reverse("org-write", args=[self.org.pk])
            )
            self.assertEqual(response.status_code, 200)

    def test_write_denies_observer_and_non_member(self):
        for user in (self.observer, self.outsider):
            self.client.force_login(user)
            response = self.client.post(
                reverse("org-write", args=[self.org.pk])
            )
            self.assertEqual(response.status_code, 403)

    def test_delete_allows_admin_only(self):
        self.client.force_login(self.admin)
        response = self.client.post(
            reverse("org-delete", args=[self.org.pk])
        )
        self.assertEqual(response.status_code, 200)

    def test_delete_denies_non_admin(self):
        for user in (self.organizer, self.observer, self.outsider):
            self.client.force_login(user)
            response = self.client.post(
                reverse("org-delete", args=[self.org.pk])
            )
            self.assertEqual(response.status_code, 403)
            