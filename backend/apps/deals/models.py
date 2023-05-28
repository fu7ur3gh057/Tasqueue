from django.db import models
from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_enum_choices.fields import EnumChoiceField

from apps.base.models import UUIDTimeStampedMixin, AnswerableMixin, FileMixin, UUIDMixin
from django.core.validators import MaxValueValidator, MinValueValidator

from apps.services.models import Service
# from apps.locations.models import Location
from apps.workers.models import Worker
from other.enums import DealStatus, OfferInitiative

User = get_user_model()

Customer = 'customers.Customer'


class Deal(UUIDTimeStampedMixin):
    owner = models.ForeignKey(Customer, related_name='deals', on_delete=models.CASCADE)
    worker = models.ForeignKey(Worker, related_name='deals', on_delete=models.CASCADE)
    services = models.ManyToManyField(Service, related_name='deals')
    title = models.CharField(max_length=100)
    description = models.TextField()
    amount = models.DecimalField(
        max_digits=5, decimal_places=2, default=0,
        validators=[MinValueValidator(10),
                    MaxValueValidator(1000)],
    )
    start_time = models.DateTimeField()
    deadline = models.DateTimeField()
    status = EnumChoiceField(DealStatus, default=DealStatus.CREATED)
    is_deleted = models.BooleanField(default=False)
    # location = models.OneToOneField(Location, related_name='deals', on_delete=models.CASCADE, null=True)
    score = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        validators=[MinValueValidator(1),
                    MaxValueValidator(10)],
        default=0
    )

    class Meta:
        verbose_name = _("Deal")
        verbose_name_plural = _("Deals")

    def __str__(self) -> str:
        return self.title


class Gallery(UUIDTimeStampedMixin):
    deal = models.OneToOneField(Deal, related_name='gallery', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()

    class Meta:
        verbose_name = _("Gallery")
        verbose_name_plural = _("Galleries")


class Image(FileMixin, UUIDMixin):
    gallery = models.ForeignKey(Gallery, related_name='images', on_delete=models.CASCADE)
    file_name = models.CharField(max_length=255)
    file = models.ImageField(upload_to='media/deals/galleries/', null=True, blank=True)

    class Meta:
        verbose_name = _("Image")
        verbose_name_plural = _("Images")


class Review(UUIDTimeStampedMixin, AnswerableMixin):
    sender = models.ForeignKey(User, related_name='sent_reviews', on_delete=models.CASCADE)
    deal = models.ForeignKey(Deal, related_name='reviews', on_delete=models.CASCADE)
    text = models.TextField()

    class Meta:
        verbose_name = _("Review")
        verbose_name_plural = _("Reviews")


class Offer(UUIDTimeStampedMixin):
    deal = models.ForeignKey(Deal, related_name='offers', on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, related_name='offers', on_delete=models.CASCADE)
    worker = models.ForeignKey(Worker, related_name='offers', on_delete=models.CASCADE)
    initiative = EnumChoiceField(OfferInitiative, default=OfferInitiative.CUSTOMER)
    text = models.TextField(blank=False)

    class Meta:
        verbose_name = _("Offer")
        verbose_name_plural = _("Offers")
