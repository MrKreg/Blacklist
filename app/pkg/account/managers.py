from django.contrib.auth.base_user import BaseUserManager
from django.db.models import QuerySet
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    _queryset_class = QuerySet

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_('Enter the email'))

        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        user = self.create_user(email, password, **extra_fields)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
