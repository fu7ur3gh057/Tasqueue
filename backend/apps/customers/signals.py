from django.db.models.signals import post_save
from django.dispatch import receiver

from django.contrib.auth import get_user_model

from apps.customers.models import Customer
from other.enums import UserType

User = get_user_model()


# Create customer after user creating
@receiver(post_save, sender=User)
def create_customer(sender, instance, created, **kwargs):
    if created and instance.type == UserType.CUSTOMER:
        Customer.objects.create(owner=instance)
