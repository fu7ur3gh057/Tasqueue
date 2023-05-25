from django_countries.serializer_fields import CountryField
from rest_framework import serializers
from django.contrib.auth import get_user_model

from apps.categories.models import Category

User = get_user_model()


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['pkid', 'name', 'tags']


class CategoryListSerializer(serializers.ModelSerializer):
    workers_count = serializers.SerializerMethodField(read_only=True)
    # deals_count = serializers.SerializerMethodField(read_only=True)
    children = serializers.SerializerMethodField(read_only=True)

    def get_children(self, obj):
        queryset = obj.children
        serializer = self.__class__(queryset, many=True)
        return serializer.data

    def get_workers_count(self, obj) -> int:
        return len(obj.workers.all())

    # def get_deals_count(self, obj) -> int:
    #     return len(obj.deals.all())

    class Meta:
        model = Category
        fields = [
            'id',
            'pkid',
            'name',
            'description',
            'tags',
            'details',
            'children',
            'workers_count',
            # 'deals_count'
        ]


class CategoryTreeSerializer(serializers.ModelSerializer):
    parent = serializers.SerializerMethodField()
    children = serializers.SerializerMethodField()
    root = serializers.SerializerMethodField()

    def get_children(self, obj):
        queryset = obj.children
        serializer = self.__class__(queryset, many=True)
        return serializer.data

    def get_parent(self, obj) -> str | None:
        parent = obj.parent
        if not parent:
            return None
        return parent.name

    def get_root(self, obj) -> str | None:
        root = obj.get_root()
        if not root:
            return None
        return root.name

    class Meta:
        model = Category
        fields = [
            'pkid',
            'name',
            'root',
            'parent',
            'children',
        ]
