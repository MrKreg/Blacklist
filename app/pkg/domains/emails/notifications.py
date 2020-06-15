from django.utils.translation import ugettext_lazy as _

from app.pkg.common.emails.service import EmailNotification


class RequestApprovedNotify(EmailNotification):
    template_name = 'emails/domains/requests/request_approved.html'
    subject = _('Your request was approved')


class RequestRefusedNotify(EmailNotification):
    template_name = 'emails/domains/requests/request_refused.html'
    subject = _('Your request was refused')
