import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _


class UUIDTimeStampedMixin(models.Model):
    pkid = models.BigAutoField(primary_key=True, editable=False)
    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UUIDMixin(models.Model):
    pkid = models.BigAutoField(primary_key=True, editable=False)
    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    class Meta:
        abstract = True


class TimeStampedMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class FileMixin(models.Model):
    name = models.CharField(max_length=255)
    path = models.CharField(max_length=255)

    class Meta:
        abstract = True


class AnswerableMixin(models.Model):
    is_answer = models.BooleanField(default=False)
    answer_to = models.ForeignKey(
        'self',
        related_name='answers',
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )

    class Meta:
        abstract = True


class BeatMixin(TimeStampedMixin):
    pkid = models.BigAutoField(primary_key=True, editable=False)

    class Meta:
        abstract = True


class AchievementMixin(models.Model):
    pkid = models.BigAutoField(primary_key=True, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=False)
    icon = models.ImageField(upload_to='/achievements')

    class Meta:
        abstract = True

