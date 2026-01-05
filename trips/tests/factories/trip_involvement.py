import factory

from organizations.tests.factories import PersonFactory
from trips.models import TripInvolvement
from trips.tests.factories import TripFactory


class TripInvolvementFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = TripInvolvement

    trip = factory.SubFactory(TripFactory)
    person = factory.SubFactory(PersonFactory)
    status = TripInvolvement.Status.ATTENDING
