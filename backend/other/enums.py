from enum import Enum, IntEnum


class FileType(str, Enum):
    AUDIO = "audio"
    IMAGE = "image"
    VIDEO = "video"
    DOCUMENT = "document"
    OTHER = "other"


class DealStatus(str, Enum):
    CREATED = "created"
    CONFIRMED = 'confirmed'
    PROCESSING = 'processing'
    COMPLETED = 'completed'


class OfferType(str, Enum):
    CUSTOMER = 'customer_to_worker'
    WORKER = 'worker_to_customer'


class SubscriptionType(str, Enum):
    ACTIVE = "active"
    EXPIRED = "expired"
    CANCELED = "canceled"


class TaskPriority(IntEnum):
    EXTRA_LOW = 1
    LOW = 3
    MEDIUM = 5
    HIGH = 7
    EXTRA_HIGH = 9


class UserType(str, Enum):
    CUSTOMER = "customer"
    WORKER = "worker"
