from django.conf import settings
from django.db import models


class TimeStampedModel(models.Model):
    """
    Abstract base model that adds created_at / modified_at timestamps.
    """
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Organization(TimeStampedModel):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


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
                fields=["organization", "email", "first_name", "last_name"],
                name="unique_user_per_org_person",
                condition=models.Q(user__isnull=False),
            )
        ]

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.organization.name})"


class UserProfile(TimeStampedModel):
    """
    Account-holder profile shared across all organizations.
    """

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile",
    )

    first_name = models.CharField(max_length=80, blank=True)
    last_name = models.CharField(max_length=120, blank=True)
    email = models.EmailField(blank=False)
    phone = models.CharField(max_length=15, blank=True)

    # future:
    # avatar = models.ImageField(...)
    # preferences = models.JSONField(...)

    def __str__(self):
        return f"{self.first_name} {self.last_name}" or self.user.get_username()
