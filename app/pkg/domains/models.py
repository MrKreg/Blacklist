from django.db import models
from django.utils.translation import ugettext_lazy as _
from django_extensions.db.models import TimeStampedModel

from app.pkg.domains.choices import Status


class BlockedDomain(TimeStampedModel):
    domain = models.CharField(_('ip/domain to block'), max_length=100, unique=True)

    class Meta:
        verbose_name = _('blocked domain')
        verbose_name_plural = _('blocked domains')


class BlockRequest(TimeStampedModel):
    domain = models.CharField(_('ip/domain to block'), max_length=100)
    user_email = models.EmailField(_("user's email"))
    user_ip = models.GenericIPAddressField()
    description = models.TextField(_('reason to block'))
    status = models.PositiveSmallIntegerField(
        verbose_name=_('request status'),
        choices=Status.choices(), default=Status.CREATED.value
    )

    class Meta:
        verbose_name = _('block request')
        verbose_name_plural = _('blocked domains')

    @property
    def is_approved(self):
        return self.status == Status.APPROVED.value

    @property
    def is_refused(self):
        return self.status == Status.REFUSED.value
