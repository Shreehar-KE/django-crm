from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    is_approved = models.BooleanField(
        default=False, null=True, blank=True)
    approval_status = models.CharField(
        max_length=20,
        choices=[
            ("pending", "Pending"),
            ("approved", "Approved"),
            ("rejected", "Rejected"),
        ],
        default="pending",
    )
    def save(self, *args, **kwargs):
        if self.approval_status in ["pending", "rejected"]:
            self.is_approved = False
        else:
            self.is_approved= True
        super().save(*args, **kwargs)

    def clean(self):
        return super().clean()
