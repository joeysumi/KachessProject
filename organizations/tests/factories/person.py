import factory
from organizations.models import Person
from .user import UserFactory
from .organization import OrganizationFactory


class PersonFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Person

    user = factory.SubFactory(UserFactory)
    organization = factory.SubFactory(OrganizationFactory)
    first_name = factory.Sequence(lambda n: f"first-{n}")
    last_name = factory.Sequence(lambda n: f"last-{n}")
