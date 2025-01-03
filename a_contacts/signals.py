from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

from .models import Contact, Event


@receiver(post_save, sender=Contact)
def track_contact_save(sender, instance, created, **kwargs):
    if created:
        action = "CREATE_CONTACT"
    else: 
        action = "UPDATE_CONTACT"
    if instance.is_deleted:
        action = "DELETE_CONTACT"
    Event.objects.create(contact=instance, user=instance.updated_by, action=action)

