from django.conf import settings
from django.db import models
from .organization import Organization
from .base import TimeStampedModel

User = settings.AUTH_USER_MODEL

class Person(TimeStampedModel):
    """
    A human known by exactly one organization.
    May or may not be linked to a registered User.
    """

    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="people",
    )

    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="person_links",
        help_text="Optional link to a registered account",
    )

    first_name = models.CharField(max_length=80, blank=False)
    last_name = models.CharField(max_length=120, blank=True)
    preferred_name = models.CharField(max_length=80, blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=15, blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        constraints = [
            # Prevent the same user being linked twice *within* an org
            models.UniqueConstraint(
                fields=["organization", "user"],
                name="unique_user_per_org_person",
                condition=models.Q(user__isnull=False),
            )
        ]

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.organization.name})"
