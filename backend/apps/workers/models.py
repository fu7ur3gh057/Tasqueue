from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.base.models import UUIDTimeStampedMixin, FileMixin, UUIDMixin, AnswerableMixin
from apps.categories.models import Category

User = get_user_model()


class Worker(UUIDTimeStampedMixin):
    owner = models.OneToOneField(
        User, related_name='worker', on_delete=models.CASCADE
    )
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    category_list = models.ManyToManyField(Category, related_name='workers')
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

    def save(self, *args, **kwargs):
        result: list[Category] = self.category_list
        for category in self.category_list.all():
            if category.is_root_node():
                continue
            ancestors = [i for i in category.get_ancestors() if i not in result]
            result.extend(ancestors)
        self.category_list = result
        super().save()

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

