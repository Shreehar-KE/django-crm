from django.db import models
from django.urls import reverse


class Contact(models.Model):

    class Type(models.TextChoices):
        LEAD = 'LEAD', 'lead'
        PROSPECT = 'PROSPECT', 'prospect'
        CUSTOMER = 'CUSTOMER', 'customer'

    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    type = models.CharField(
        max_length=8, choices=Type.choices)

    date_time_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.first_name.title() + ' ' + self.last_name.title()

    def get_absolute_url(self):
        return reverse("a_contacts:customer-detail", kwargs={"pk": self.pk})


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
