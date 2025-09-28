# subscriptions/models.py
from django.db import models
from django.contrib.auth.models import User
from core.models import BaseModel


class Subscription(BaseModel):
    PLAN_CHOICES = [
        ("free", "Free"),
        ("basic", "Basic"),
        ("premium", "Premium"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.EmailField()
    plan = models.CharField(max_length=20, choices=PLAN_CHOICES, default="free")
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username} - {self.plan} ({'Active' if self.active else 'Inactive'})"
