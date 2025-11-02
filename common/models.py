

import uuid
from django.db import models


# ===================== Base Model =====================
class BaseModel(models.Model):
    """
    Abstract model providing a secure UUID primary key.
    Use this when you only need the unique ID.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


# ===================== Timestamped Model =====================
class TimestampedModel(models.Model):
    """
    Abstract model that automatically adds created/updated timestamps.
    Use this to track when an object was created or modified.
    """

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


# ===================== Core Model =====================
class CoreModel(BaseModel, TimestampedModel):
    """
    Combines BaseModel (UUID) and TimestampedModel (timestamps)
    into one fully reusable abstract base model for all apps.
    """

    class Meta:
        abstract = True
