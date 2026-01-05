from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase

from organizations.models import Organization, Person
from trips.models import Trip, TripInvolvement


class TestTripInvolvement(TestCase):

    def setUp(self):
        self.org_a = Organization.objects.create(name="Org A")
        self.org_b = Organization.objects.create(name="Org B")

        self.person_a = Person.objects.create(
            organization=self.org_a,
            first_name="Alice",
            last_name="OrgA",
        )

        self.person_b = Person.objects.create(
            organization=self.org_b,
            first_name="Bob",
            last_name="OrgB",
        )

        self.trip_a = Trip.objects.create(
            organization=self.org_a,
            name="Trip A",
            start_date="2026-01-01",
            end_date="2026-01-05",
        )

        self.trip_b = Trip.objects.create(
            organization=self.org_b,
            name="Trip B",
            start_date="2026-02-01",
            end_date="2026-02-05",
        )

    def test_person_can_be_involved_in_trip_from_same_org(self):
        involvement = TripInvolvement(
            trip=self.trip_a,
            person=self.person_a,
            status=TripInvolvement.Status.ATTENDING,
        )

        # Should not raise
        involvement.save()

        self.assertEqual(TripInvolvement.objects.count(), 1)

    def test_person_cannot_be_involved_in_trip_from_different_org(self):
        involvement = TripInvolvement(
            trip=self.trip_a,
            person=self.person_b,  # different org
            status=TripInvolvement.Status.INTERESTED,
        )

        with self.assertRaises(ValidationError):
            involvement.save()

        self.assertEqual(TripInvolvement.objects.count(), 0)

    def test_full_clean_is_called_on_save(self):
        """This test proves you didn’t just rely on admin forms."""
        involvement = TripInvolvement(
            trip=self.trip_b,
            person=self.person_a,
            status=TripInvolvement.Status.CONSIDERING,
        )

        with self.assertRaises(ValidationError):
            involvement.save()
