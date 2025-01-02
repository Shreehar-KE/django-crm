from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

from .models import Contact, Event


@receiver(post_save, sender=Contact)
def track_contact_save(sender, instance, created, **kwargs):
    action = "CREATE_CONTACT" if created else "UPDATE_CONTACT"
    Event.objects.create(contact=instance, user=instance.updated_by, action=action)


@receiver(pre_delete, sender=Contact)
def track_contact_delete(sender, instance, **kwargs):
    Event.objects.create(
        contact=instance, user=instance.updated_by, action="DELETE_CONTACT"
    )
