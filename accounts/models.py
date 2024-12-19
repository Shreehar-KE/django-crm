from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    is_approved = models.BooleanField(
        default=False, null=True, blank=True, editable=True
    )

    def clean(self):
        return super().clean()
