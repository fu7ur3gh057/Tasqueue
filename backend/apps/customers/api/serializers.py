from django_countries.serializer_fields import CountryField
from rest_framework import serializers
from django.contrib.auth import get_user_model

from apps.customers.models import Customer

User = get_user_model()


class CustomerSerializer(serializers.ModelSerializer):
    owner_id = serializers.CharField(source='owner.id', read_only=True)
    email = serializers.CharField(source='owner.email', read_only=True)
    phone_number = serializers.CharField(source='owner.phone_number', read_only=True)

    class Meta:
        model = Customer
        fields = [
            'id',
            'owner_id',
            'email',
            'phone_number',
            'first_name',
            'last_name',
            'birthdate',
            'photo',
            'city',
            'is_subscribed'
        ]


class CustomerUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = [
            'first_name',
            'last_name',
            'birthdate',
            'photo',
            'city'
        ]
