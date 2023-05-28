from rest_framework.pagination import PageNumberPagination


class ServicePagination(PageNumberPagination):
    page_size = 9
