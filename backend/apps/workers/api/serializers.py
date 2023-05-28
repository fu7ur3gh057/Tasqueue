from django.contrib.auth import get_user_model
from rest_framework import serializers

from apps.services.api.serializers import ServiceSerializer
from apps.workers.models import Worker

User = get_user_model()


class WorkerSerializer(serializers.ModelSerializer):
    owner_id = serializers.CharField(source='owner.id', read_only=True)
    email = serializers.CharField(source='owner.email', read_only=True)
    phone_number = serializers.CharField(source='owner.phone_number', read_only=True)
    services = ServiceSerializer(read_only=True, many=True)

    class Meta:
        model = Worker
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
            'services',
        ]


class WorkerUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Worker
        fields = [
            'first_name',
            'last_name',
            'birthdate',
            'photo',
            'city',
            'experience',
        ]
