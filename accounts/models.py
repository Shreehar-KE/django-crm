import uuid

from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator, validate_email
from django.db import models
from django.urls import reverse
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill


class CustomUser(AbstractUser):

    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        MANAGER = "MANAGER", "Manager"
        AGENT = "AGENT", "Agent"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    image = models.ImageField(
        upload_to="employee-avatars/",
        null=True,
        blank=True,
        validators=[
            FileExtensionValidator(allowed_extensions=["PNG", "JPEG", "WebP", "JPG"])
        ],
    )
    image_thumbnail = ImageSpecField(
        source="image",
        processors=[ResizeToFill(100, 100)],
        format="JPEG",
        options={"quality": 60},
    )
    email = models.EmailField(unique=True, validators=[validate_email])
    location = models.CharField(max_length=255, null=True, blank=True)
    role = models.CharField(max_length=8, choices=Role.choices, default=Role.AGENT)
    employee_id = models.BigIntegerField(
        unique=True, null=True, blank=True, editable=False
    )
    is_approved = models.BooleanField(default=False, null=True, blank=True)
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
            self.is_approved = True
        if not self.employee_id:
            self.employee_id = self.generate_employee_id()
        super().save(*args, **kwargs)

    def clean(self):
        return super().clean()

    def get_absolute_url(self):
        return reverse("accounts:employee-detail", kwargs={"pk": self.pk})

    def generate_employee_id(self):
        return EmployeeIDCounter.get_next_employee_id()

    def __str__(self):
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        else:
            return f"@{self.username}"


class EmployeeIDCounter(models.Model):
    current_id = models.PositiveIntegerField(default=100000)

    @classmethod
    def get_next_employee_id(cls):
        counter, created = cls.objects.get_or_create(pk=1)
        counter.current_id += 1
        counter.save()
        return counter.current_id
