from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

# from apps.achievements.models import CustomerAchievement
from apps.base.models import UUIDTimeStampedMixin
from apps.deals.models import Offer
from other.enums import OfferInitiative

User = get_user_model()


class Customer(UUIDTimeStampedMixin):
    owner = models.OneToOneField(
        User, related_name='customer', on_delete=models.CASCADE
    )
    # achievements = models.ForeignKey(
    #     CustomerAchievement, related_name='customers', on_delete=models.SET_NULL, null=True
    # )
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    birthdate = models.DateField(blank=True, null=True)
    photo = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=20, null=True, blank=True)
    is_subscribed = models.BooleanField(default=False)

    @property
    def full_name(self) -> str:
        return f'{self.first_name} {self.last_name}'

    @property
    def phone_number(self) -> str:
        return f'{self.owner.phone_number}'

    @property
    def my_offers(self) -> list[Offer] | None:
        return self.offers.filter(initiative=OfferInitiative.CUSTOMER)

    @property
    def receive_offers(self) -> list[Offer] | None:
        return self.offers.filter(initiative=OfferInitiative.WORKER)

    def __str__(self) -> str:
        return self.owner.email

    class Meta:
        verbose_name = _("Customer")
        verbose_name_plural = _("Customer")
