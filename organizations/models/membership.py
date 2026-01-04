from django.conf import settings
from django.db import models
from .organization import Organization
from .base import TimeStampedModel

User = settings.AUTH_USER_MODEL


class OrganizationMembership(TimeStampedModel):
    
    class Role(models.TextChoices):
        ADMIN = "admin", "Admin" # Full organization control
        ORGANIZER = "organizer", "Organizer" # Control over everything in an organization except delete
        OBSERVER = "observer", "Observer" # Access to view everything but cannot add/edit/remove

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="organization_memberships",
    )
    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="memberships",
    )
    role = models.CharField(
        max_length=20,
        choices=Role.choices,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "organization"],
                name="unique_user_per_organization",
            )
        ]

    def __str__(self):
        return f"{self.user} → {self.organization} ({self.role})"
