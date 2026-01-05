import factory

from organizations.tests.factories import OrganizationFactory
from trips.models import Trip


class TripFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Trip

    organization = factory.SubFactory(OrganizationFactory)
    name = factory.Sequence(lambda n: f"trip{n}")
    start_date = factory.Sequence(lambda n: f"2025-01-{n + 10}")
    end_date = factory.Sequence(lambda n: f"2025-01-{n + 12}")
