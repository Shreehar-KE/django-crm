import uuid
from django.db import models
from django.conf import settings
from django.core.validators import FileExtensionValidator, validate_email
from django.urls import reverse
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill


class Contact(models.Model):

    class Type(models.TextChoices):
        LEAD = "LEAD", "Lead"
        PROSPECT = "PROSPECT", "Prospect"
        CUSTOMER = "CUSTOMER", "Customer"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    name = models.CharField(max_length=512, null=True, blank=True, editable=False)
    image = models.ImageField(
        upload_to="avatars/",
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
    type = models.CharField(max_length=8, choices=Type.choices, default=Type.LEAD)
    contact_id = models.BigIntegerField(
        unique=True, null=True, blank=True, editable=False
    )
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True
    )

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.first_name.title() + " " + self.last_name.title()

    def save(self, *args, **kwargs):
        self.name = f"{self.first_name.lower()} {self.last_name.lower()}"
        if not self.contact_id:
            self.contact_id = self.generate_contact_id()
        super().save(*args, **kwargs)

    def generate_contact_id(self):
        return ContactIDCounter.get_next_contact_id()

    def get_absolute_url(self):
        return reverse("a_contacts:contact-detail", kwargs={"pk": self.pk})


class ContactIDCounter(models.Model):
    current_id = models.PositiveIntegerField(default=0)

    @classmethod
    def get_next_contact_id(cls):
        counter, created = cls.objects.get_or_create(pk=1)
        counter.current_id += 1
        counter.save()
        return counter.current_id


class LeadManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(type=Contact.Type.LEAD)
        return queryset


class Lead(Contact):
    class Meta:
        proxy = True

    objects = LeadManager()

    def get_absolute_url(self):
        return reverse("a_contacts:contact-detail", kwargs={"pk": self.pk})


class ProspectManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(type=Contact.Type.PROSPECT)
        return queryset


class Prospect(Contact):
    class Meta:
        proxy = True

    objects = ProspectManager()

    def get_absolute_url(self):
        return reverse("a_contacts:contact-detail", kwargs={"pk": self.pk})


class CustomerManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(type=Contact.Type.CUSTOMER)
        return queryset


class Customer(Contact):
    class Meta:
        proxy = True

    objects = CustomerManager()

    def get_absolute_url(self):
        return reverse("a_contacts:contact-detail", kwargs={"pk": self.pk})
