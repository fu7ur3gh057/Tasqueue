from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django_enum_choices.fields import EnumChoiceField
from phonenumber_field.modelfields import PhoneNumberField

from apps.base.models import UUIDTimeStampedMixin
from apps.users.managers import UserManager
from other.enums import RoleType


class User(AbstractBaseUser, PermissionsMixin, UUIDTimeStampedMixin):
    phone_number = PhoneNumberField(
        verbose_name=_('Phone Number'),
        null=False,
        unique=True
    )
    email = models.CharField(
        verbose_name=_('Email'),
        max_length=50,
        null=False,
        unique=True
    )
    role = EnumChoiceField(RoleType, default=RoleType.CUSTOMER)

    is_verified = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = UserManager()
    USERNAME_FIELD = "email"

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    def __str__(self):
        return self.email
