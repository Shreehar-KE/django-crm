from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site
from django.core.mail import send_mail
from django.db.models.signals import pre_save
from django.dispatch import receiver



@receiver(pre_save, sender=get_user_model())
def send_approval_email(sender, instance, **kwargs):
    try:
        previous_instance = sender.objects.get(pk=instance.pk)
    except sender.DoesNotExist:
        return
    if previous_instance.username != settings.ADMIN_NAME:
        if (
            previous_instance.approval_status != "approved"
            and instance.approval_status == "approved"
        ):
            site_url = Site.objects.get_current().domain
            send_mail(
                subject="Your Django CRM Account Has Been Approved",
                message=f"Dear {instance.username},\n\nYour Django CRM account has been approved. You can now access all the features of the application.\nVisit the application at { site_url }.\n\nThank you!",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[instance.email],
                fail_silently=False,
            )
        if (
            previous_instance.approval_status != "rejected"
            and instance.approval_status == "rejected"
        ):
            site_url = Site.objects.get_current().domain
            send_mail(
                subject="Your Django CRM Account Has Been Rejected",
                message=f"Dear {instance.username},\n\nYour Django CRM account signup has been rejected.\n\nThank you!",
                html_message=f'Dear {instance.username},\n\nYour Django CRM account signup has been rejected. For further info, reach out on <a class="underline text-blue-500" href="https://www.linkedin.com/in/shreehar-ke/" target="_blank">LinkedIn</a>.\n\nThank you!',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[instance.email],
                fail_silently=False,
            )
