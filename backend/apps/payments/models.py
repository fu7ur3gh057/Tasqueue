from typing import Any

from django.db import models
from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_enum_choices.fields import EnumChoiceField
import datetime
from apps.base.models import UUIDMixin, UUIDTimeStampedMixin
from other.enums import SubscriptionType

User = get_user_model()


class Wallet(UUIDMixin):
    owner = models.OneToOneField(User, related_name='wallet', on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=5, decimal_places=2, default=1.20)

    # bonus_amount = models.IntegerField(default=0)

    class Meta:
        verbose_name = _("Wallet")
        verbose_name_plural = _("Wallets")

    @property
    def email(self) -> str:
        return self.owner.email

    @property
    def bonus_amount(self) -> int:
        amount = 0
        bonuses = self.bonuses
        if bonuses is None:
            return amount
        for bonus in bonuses:
            amount += bonus.amount
        return amount

    @property
    def active_subscription(self) -> Any:
        subscriptions = self.subscriptions
        if subscriptions is None:
            return None
        active = subscriptions.all().filter(type=SubscriptionType.ACTIVE).first()
        return active

    def __str__(self) -> str:
        return f'{self.email}'


class Transaction(UUIDTimeStampedMixin):
    wallet = models.ForeignKey(Wallet, related_name='transactions', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=5, decimal_places=2, default=1)

    class Meta:
        verbose_name = _("Transaction")
        verbose_name_plural = _("Transactions")

    def __str__(self) -> str:
        return f'{self.wallet}'


class Subscription(UUIDTimeStampedMixin):
    wallet = models.ForeignKey(Wallet, related_name='subscriptions', on_delete=models.CASCADE)
    type = EnumChoiceField(SubscriptionType, default=SubscriptionType.ACTIVE)
    end_time = models.DateTimeField(auto_now=False, auto_now_add=False, blank=True, null=True)

    class Meta:
        verbose_name = _("Subscription")
        verbose_name_plural = _("Subscriptions")

    def save(self, *args, **kwargs):
        super().save()
        save_date = self.created_at
        year = save_date.year
        month = save_date.month + 1
        day = save_date.day
        if month > 12:
            month = 1
            year += 1
        self.end_time = datetime.datetime(year, month, day)
        super().save()


class Bonus(UUIDTimeStampedMixin):
    wallet = models.ForeignKey(User, related_name='bonuses', on_delete=models.CASCADE)
    amount = models.IntegerField(default=5)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name = _("Bonus")
        verbose_name_plural = _("Bonuses")
