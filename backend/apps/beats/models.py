from django.db import models

from apps.base.models import BeatMixin


# Subscription Expiration
class ExpirationBeat(BeatMixin):
    pass


# Deal Deadline
class DeadlineBeat(BeatMixin):
    pass


class NotificationBeat(BeatMixin):
    pass
