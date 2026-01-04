from django.db import models


class TimeStampedModel(models.Model):
    """
    Abstract base model that adds created_at / modified_at timestamps.
    """
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
