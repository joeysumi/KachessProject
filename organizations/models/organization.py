from django.db import models
from .base import TimeStampedModel

import random

from organizations.utils import get_random_string

class Organization(TimeStampedModel):
    name = models.CharField(max_length=128)
    unique_name = models.CharField(max_length=255, blank=True, unique=True)

    def __str__(self):
        return self.unique_name
    
    def save(self, *args, **kwargs):
        if not self.unique_name:
            self._get_unique_org_name()

        super().save(*args, **kwargs)
    
    def _get_unique_org_name(self):
        unique_name = self._create_unique_name()
        if self._unique_name_already_exists(unique_name):
            unique_name = unique_name + str(random.randint(1, 10))
            
        self.unique_name = unique_name
    
    def _create_unique_name(self):
        snake_case_name = self.name.replace(" ", "_").lower()
        random_str = get_random_string(6)
        return snake_case_name + random_str

    def _unique_name_already_exists(self, unique_name):
        return Organization.objects.filter(unique_name=unique_name).exclude(pk=self.pk).exists()
