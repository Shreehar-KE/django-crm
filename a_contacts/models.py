import uuid
from django.db import models
from django.urls import reverse


class Contact(models.Model):

    class Type(models.TextChoices):
        LEAD = 'LEAD', 'Lead'
        PROSPECT = 'PROSPECT', 'Prospect'
        CUSTOMER = 'CUSTOMER', 'Customer'
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='avatars/', null=True, blank=True)
    email = models.EmailField(unique=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    type = models.CharField(
        max_length=8, choices=Type.choices, default=Type.LEAD)
    contact_id = models.BigIntegerField(
        unique=True, null=True, blank=True, editable=False)
    date_time_added = models.DateTimeField(auto_now_add=True, editable=False)
    name = models.CharField(max_length=512, null=True,
                            blank=True, editable=False)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.first_name.title() + ' ' + self.last_name.title()

    def save(self, *args, **kwargs):
        self.name = f"{self.first_name.lower()} {self.last_name.lower()}"
        if not self.contact_id:
            last_contact = Contact.objects.order_by('-contact_id').first()
            if last_contact:
                next_id = last_contact.contact_id + 1
            else:
                next_id = 1
            self.contact_id = next_id
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("a_contacts:contact-detail", kwargs={"pk": self.pk})


class LeadManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(
            type=Contact.Type.LEAD)
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
        queryset = queryset.filter(
            type=Contact.Type.PROSPECT)
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
        queryset = queryset.filter(
            type=Contact.Type.CUSTOMER)
        return queryset


class Customer(Contact):
    class Meta:
        proxy = True
    objects = CustomerManager()

    def get_absolute_url(self):
        return reverse("a_contacts:contact-detail", kwargs={"pk": self.pk})
