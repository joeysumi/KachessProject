from django.db import models

from organizations.models import Organization, TimeStampedModel

from utils import get_unique_name

class Trip(TimeStampedModel):
    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="trips",
    )

    name = models.CharField(max_length=128)
    unique_name = models.CharField(max_length=255, blank=True, unique=True)

    start_date = models.DateField()
    end_date = models.DateField()
    location = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.name} ({self.organization})"

    def save(self, *args, **kwargs):
        if not self.unique_name:
            self.unique_name = self._get_unique_trip_name()
        
        super().save(*args, **kwargs)
    
    def _get_unique_trip_name(self):
        while True:
            unique_name = get_unique_name(name=self.name, random_length=10)
            if not Trip.objects.filter(unique_name=unique_name).exclude(pk=self.pk).exists():
                return unique_name
    