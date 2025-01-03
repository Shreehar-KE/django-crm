from django.apps import apps
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender="a_contacts.Contact")
def track_contact_save(sender, instance, created, **kwargs):
    Event = apps.get_model("a_contacts", "Event")

    if created:
        action = Event.Action.CREATE
    elif not instance.last_action:
        action = Event.Action.UPDATE
    else:
        action = instance.last_action
    Event.objects.create(contact=instance, user=instance.updated_by, action=action)
