from django.test import TestCase
from organizations.tests.factories import OrganizationFactory
from unittest.mock import patch

class TestOrganization(TestCase):

    def test_save__unique_name_automatically_populates_if_not_given(self):
        new_org = OrganizationFactory(name="Test Org")
        
        self.assertIsNotNone(new_org.unique_name)

    @patch("organizations.models.organization.get_unique_name")
    def test_save__unique_name_cycles_anew_if_unique_name_already_exists(self, mock_name_generator):
        first_unique_name = "test1234"
        second_unique_name = "test2345"
        mock_name_generator.side_effect = [first_unique_name, first_unique_name, second_unique_name]  # edge case, but try three times
        org_a = OrganizationFactory.create(name="Test Org", unique_name=first_unique_name)
        org_b = OrganizationFactory.create(name="Test Org")

        self.assertEqual(mock_name_generator.call_count, 3)
        self.assertTrue(org_a.unique_name != org_b.unique_name)
