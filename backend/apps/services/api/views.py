import django_filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status, filters
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.services.api.serializers import ServiceListSerializer, ServiceTreeSerializer
from apps.services.exceptions import ServiceNotFound
from apps.services.models import Service
from apps.services.pagination import ServicePagination


class ServiceFilter(django_filters.FilterSet):
    id = django_filters.CharFilter(field_name='id', lookup_expr='iexact')
    name = django_filters.CharFilter(field_name='name', lookup_expr='iexact')


class ServiceTreeFilter(django_filters.FilterSet):
    id = django_filters.CharFilter(field_name='id', lookup_expr='iexact')
    name = django_filters.CharFilter(field_name='name', lookup_expr='iexact')
    root = django_filters.CharFilter(field_name='root', lookup_expr='iexact')


class ServiceListView(generics.ListAPIView):
    serializer_class = ServiceListSerializer
    queryset = Service.objects.all()
    pagination_class = ServicePagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = ServiceFilter
    search_fields = ['id', 'name']

    def get_queryset(self) -> list[Service]:
        return self.queryset.filter(parent=None)


class ServiceTreeView(generics.ListAPIView):
    serializer_class = ServiceTreeSerializer
    queryset = Service.objects.all()
    pagination_class = ServicePagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = ServiceFilter
    search_fields = ['id', 'name']

    def get_queryset(self) -> list[Service]:
        return self.queryset.filter(parent__isnull=True)


class ServiceView(APIView):
    serializer_class = ServiceTreeSerializer

    def get(self, request: Request, service_id: str) -> Response:
        services = Service.objects.get(id=service_id)
        if not services:
            raise ServiceNotFound()
        serializer = self.serializer_class(services)
        return Response(serializer.data, status=status.HTTP_200_OK)
