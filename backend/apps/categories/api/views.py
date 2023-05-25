import django_filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status, filters
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.categories.api.serializers import CategoryListSerializer, CategoryTreeSerializer
from apps.categories.exceptions import CategoryNotFound
from apps.categories.models import Category
from apps.categories.pagination import CategoryPagination


class CategoryFilter(django_filters.FilterSet):
    id = django_filters.CharFilter(field_name='id', lookup_expr='iexact')
    name = django_filters.CharFilter(field_name='name', lookup_expr='iexact')


class CategoryTreeFilter(django_filters.FilterSet):
    id = django_filters.CharFilter(field_name='id', lookup_expr='iexact')
    name = django_filters.CharFilter(field_name='name', lookup_expr='iexact')
    root = django_filters.CharFilter(field_name='root', lookup_expr='iexact')


class CategoryListView(generics.ListAPIView):
    serializer_class = CategoryListSerializer
    queryset = Category.objects.all()
    pagination_class = CategoryPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = CategoryFilter
    search_fields = ['id', 'name']

    def get_queryset(self) -> list[Category]:
        return self.queryset.filter(parent=None)


class CategoryTreeView(generics.ListAPIView):
    serializer_class = CategoryTreeSerializer
    queryset = Category.objects.all()
    pagination_class = CategoryPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = CategoryFilter
    search_fields = ['id', 'name']

    def get_queryset(self) -> list[Category]:
        return self.queryset.filter(parent__isnull=True)


class CategoryView(APIView):
    serializer_class = CategoryTreeSerializer

    def get(self, request: Request, service_id: str) -> Response:
        category_list = Category.objects.get(id=service_id)
        if not category_list:
            raise CategoryNotFound()
        serializer = self.serializer_class(category_list)
        return Response(serializer.data, status=status.HTTP_200_OK)
