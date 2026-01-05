from django.core.exceptions import ValidationError
from django.db import models

from organizations.models import Person, TimeStampedModel

from .trip import Trip


class TripInvolvement(TimeStampedModel):

    class Status(models.TextChoices):
        INTERESTED = "interested", "Interested"
        CONSIDERING = "considering", "Considering"
        ATTENDING = "attending", "Attending"

    trip = models.ForeignKey(
        Trip,
        on_delete=models.CASCADE,
        related_name="involvements",
    )

    person = models.ForeignKey(
        Person,
        on_delete=models.CASCADE,
        related_name="trip_involvements",
    )

    status = models.CharField(max_length=20, choices=Status.choices)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["trip", "person"],
                name="unique_person_per_trip",
            )
        ]
    
    def clean(self):
        if self.person.organization_id != self.trip.organization_id:
            raise ValidationError(
                "Person and Trip must belong to the same organization."
            )
    
    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)


    def __str__(self):
        return f"{self.person} → {self.trip} ({self.status})"
