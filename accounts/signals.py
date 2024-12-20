from django.contrib.sites.models import Site
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import CustomUser


@receiver(post_save, sender=CustomUser)
def send_approval_email(sender, instance, **kwargs):
    if instance.approval_status == "approved":
        send_mail(
            subject="Your Django CRM Account Has Been Approved",
            message=f"Dear {instance.username},\n\nYour Django CRM account has been approved. You can now access all the features of the application.\nVisit the application at http://127.0.0.1:8000.\n\nThank you!",
            from_email="admin@" + Site.objects.get_current().domain,
            recipient_list=[instance.email],
            fail_silently=False,
        )
