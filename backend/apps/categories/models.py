from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils.translation import gettext_lazy as _
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel
from apps.base.models import UUIDMixin


class Category(MPTTModel, UUIDMixin):
    name = models.CharField(max_length=255, blank=False, null=True)
    description = models.TextField(blank=True)
    tags = ArrayField(models.CharField(max_length=200), blank=True)
    details = models.JSONField(null=True, blank=True)
    default_price = models.FloatField(null=True, blank=True)

    parent = TreeForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children'
    )

    class MPTTMeta:
        order_insertion_by = ['name']

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")

    def __str__(self) -> str:
        return f'{self.name}'
