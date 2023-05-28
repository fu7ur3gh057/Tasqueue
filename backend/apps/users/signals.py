from django.db.models.signals import post_save
from django.dispatch import receiver

from django.contrib.auth import get_user_model

from apps.customers.models import Customer
from other.enums import RoleType

User = get_user_model()


# Create customer after user creating
@receiver(post_save, sender=User)
def create_user(sender, instance, created, **kwargs):
    if not created:
        return
    if instance.type == RoleType.ADMIN:
        instance.is_staff = True
        instance.is_superuser = True
    elif instance.type == RoleType.STAFF:
        instance.is_staff = True
