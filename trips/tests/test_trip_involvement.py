from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase

from organizations.tests.factories import OrganizationFactory, PersonFactory
from trips.models import TripInvolvement
from trips.tests.factories import TripFactory, TripInvolvementFactory


class TestTripInvolvement(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.org_a = OrganizationFactory(name="Org A")
        cls.org_b = OrganizationFactory(name="Org B")

        cls.person_a = PersonFactory(
            organization=cls.org_a,
        )

        cls.person_b = PersonFactory(
            organization=cls.org_b
        )

        cls.trip_a = TripFactory(
            organization=cls.org_a,
        )

        cls.trip_b = TripFactory(
            organization=cls.org_b,
        )

    def test_person_can_be_involved_in_trip_from_same_org(self):
        TripInvolvementFactory(
            trip=self.trip_a,
            person=self.person_a,
            status=TripInvolvement.Status.ATTENDING,
        )

        self.assertEqual(TripInvolvement.objects.count(), 1)

    def test_person_cannot_be_involved_in_trip_from_different_org(self):
        with self.assertRaises(ValidationError):
            TripInvolvementFactory(
                trip=self.trip_a,
                person=self.person_b, # belongs to a different org
                status=TripInvolvement.Status.INTERESTED,
            )

        self.assertEqual(TripInvolvement.objects.count(), 0)

    def test_full_clean_is_called_on_save(self):
        """This test proves you didn’t just rely on admin forms."""
        involvement = TripInvolvement(
            trip=self.trip_b,
            person=self.person_a, # belongs to a different org
            status=TripInvolvement.Status.CONSIDERING,
        )

        with self.assertRaises(ValidationError):
            involvement.save()
