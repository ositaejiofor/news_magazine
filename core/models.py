from django.db import models


class BaseModel(models.Model):
    """
    Abstract base model with timestamps, ordering, and admin-friendly names.
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ['-created_at', '-updated_at']
        verbose_name = "Base Model"
        verbose_name_plural = "Base Models"
