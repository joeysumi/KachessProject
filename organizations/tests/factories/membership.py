import factory
from organizations.models import OrganizationMembership
from .user import UserFactory
from .organization import OrganizationFactory


class OrganizationMembershipFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = OrganizationMembership

    user = factory.SubFactory(UserFactory)
    organization = factory.SubFactory(OrganizationFactory)
    role = OrganizationMembership.Role.ADMIN
