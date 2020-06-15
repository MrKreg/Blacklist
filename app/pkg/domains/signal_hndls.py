from django.dispatch import receiver
from fieldsignals import post_save_changed

from app.pkg.domains.choices import Status
from app.pkg.domains.emails.notifications import RequestApprovedNotify, RequestRefusedNotify
from app.pkg.domains.models import BlockRequest


@receiver(post_save_changed, sender=BlockRequest, fields=['status'])
def notify_user_about_review(instance, **kwargs):
    if instance.status == Status.APPROVED.value:
        RequestApprovedNotify.send_to_email(instance.user_email)
    else:
        RequestRefusedNotify.send_to_email(instance.user_email)
