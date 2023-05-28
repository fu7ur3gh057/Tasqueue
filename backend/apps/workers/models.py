from typing import Any

from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

# from apps.achievements.models import WorkerAchievement
from apps.base.models import UUIDTimeStampedMixin, FileMixin, UUIDMixin, AnswerableMixin
from apps.services.models import Service
from other.enums import OfferInitiative

User = get_user_model()


class Worker(UUIDTimeStampedMixin):
    owner = models.OneToOneField(
        User, related_name='worker', on_delete=models.CASCADE
    )
    services = models.ManyToManyField(Service, related_name='workers')
    # achievements = models.ForeignKey(
    #     WorkerAchievement, related_name='workers', on_delete=models.SET_NULL, null=True
    # )
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    photo = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=20, null=True, blank=True)
    documents_verified = models.BooleanField(default=False)
    experience = models.FloatField(default=0)
    rating = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        validators=[MinValueValidator(1),
                    MaxValueValidator(10)],
        default=0
    )

    class Meta:
        verbose_name = _("Worker")
        verbose_name_plural = _("Workers")

    @property
    def full_name(self) -> str:
        return f'{self.first_name} {self.last_name}'

    @property
    def phone_number(self) -> str:
        return f'{self.owner.phone_number}'

    @property
    def my_offers(self) -> list[Any] | None:
        return self.offers.filter(initiative=OfferInitiative.WORKER)

    @property
    def receive_offers(self) -> list[Any] | None:
        return self.offers.filter(initiative=OfferInitiative.CUSTOMER)

    # def save(self, *args, **kwargs):
    #     result: list[Service] = []
    #     for service in self.services.all():
    #         if service.is_root_node():
    #             continue
    #         root = service.parent
    #         result.append(root)
    #     self.services.add(*result)
    #     super().save()

    def __str__(self) -> str:
        return self.owner.email


class Document(FileMixin, UUIDMixin):
    owner = models.ForeignKey(Worker, related_name='documents', on_delete=models.CASCADE)
    file = models.ImageField(upload_to='media/documents/', null=True, blank=True)

    class Meta:
        verbose_name = _("Document")
        verbose_name_plural = _("Documents")


class Gallery(UUIDTimeStampedMixin):
    owner = models.ForeignKey(Worker, related_name='galleries', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()

    class Meta:
        verbose_name = _("Gallery")
        verbose_name_plural = _("Galleries")


class Image(FileMixin, UUIDMixin):
    gallery = models.ForeignKey(Gallery, related_name='images', on_delete=models.CASCADE)
    file_name = models.CharField(max_length=255)
    file = models.ImageField(upload_to='media/workers/galleries/', null=True, blank=True)

    class Meta:
        verbose_name = _("Image")
        verbose_name_plural = _("Images")
