from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils.translation import ugettext_lazy as _

from app.pkg.account.managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email'), unique=True)
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True, blank=True)

    is_staff = models.BooleanField(
        _('staff status'), default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'), default=True, db_index=True,
        help_text=_('Designates whether this user should be treated as active.'),
    )

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
