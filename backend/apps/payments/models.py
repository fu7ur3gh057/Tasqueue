from django.db import models
from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.base.models import UUIDMixin

User = get_user_model()


class Wallet(UUIDMixin):
    owner = models.OneToOneField(User, related_name='wallet', on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=5, decimal_places=2, default=1.20)

    class Meta:
        verbose_name = _("Wallet")
        verbose_name_plural = _("Wallets")

    @property
    def email(self) -> str:
        return self.owner.email

    def __str__(self) -> str:
        return f'{self.email}'
