from django.conf import settings
from django.db import models
from .base import TimeStampedModel

User = settings.AUTH_USER_MODEL

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
