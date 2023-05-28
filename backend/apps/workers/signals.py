from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.workers.models import Worker
from other.enums import RoleType

User = get_user_model()


# Create customer after user creating
@receiver(post_save, sender=User)
def create_worker(sender, instance: User, created: bool, **kwargs: dict):
    if created and instance.type == RoleType.WORKER:
        Worker.objects.create(owner=instance)


# @receiver(post_save, sender=Worker)
# def update_worker_services(sender, instance: Worker, created: bool, **kwargs: dict):
#     roots = []
#     services = instance.services.all()
#     for service in services:
#         root = service.get_root()
#         if root is None:
#             continue
#         roots.append(root)
#     for i in roots:
#         instance.services.add(i)
#     instance.save()
