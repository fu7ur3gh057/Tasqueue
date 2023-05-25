from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry

from apps.customers.models import Customer


@registry.register_document
class CustomerDocument(Document):
    owner = fields.ObjectField(properties={
        'id': fields.TextField(),
        # 'phone_number': fields.TextField(),
        'email': fields.TextField(),
    })

    class Index:
        name = 'customers'
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 0,
        }

    # def save(self, **kwargs):
    #     self.owner.phone_number = str(self.phone_number)  # Convert PhoneNumber to string
    #     return super().save(**kwargs)

    class Django:
        model = Customer
        fields = [
            'first_name',
            'last_name',
            'birthdate',
            'city',
            'photo',
        ]
