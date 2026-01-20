from django.db import models
from .base import TimeStampedModel

from utils import get_unique_name

class Organization(TimeStampedModel):
    name = models.CharField(max_length=128)
    unique_name = models.CharField(max_length=255, blank=True, unique=True)

    def __str__(self):
        return self.unique_name
    
    def save(self, *args, **kwargs):
        if not self.unique_name:
            self.unique_name = self._get_unique_org_name()

        super().save(*args, **kwargs)
    
    def _get_unique_org_name(self):
        while True:
            unique_name = get_unique_name(name=self.name, random_length=10)
            if not Organization.objects.filter(unique_name=unique_name).exclude(pk=self.pk).exists():  # validate that the generated name isn't used
                return unique_name
