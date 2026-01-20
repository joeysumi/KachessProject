from django.test import TestCase
from organizations.models import Organization
from ..utility_functions import get_unique_name, object_unique_name_already_exists

model_name = "Test Model"
snake_case_model_name = "test_model"


class TestUtilityFunctions(TestCase):
    
    def test_get_unique_name__returns_name_with_expected_features(self):
        suffix_length = 4
        name_result = get_unique_name(model_name, random_length=suffix_length)
        partitioned_name = name_result.partition(snake_case_model_name)
        
        self.assertEqual(snake_case_model_name, partitioned_name[1])
        self.assertEqual(suffix_length, len(partitioned_name[2]))
    
    # def test_object_unique_name_already_exists(self):
    # Not sure how to build this test