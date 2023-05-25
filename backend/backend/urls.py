# core/urls.py
from django.contrib import admin
from django.urls import path, include

API_URL = 'api/v3'

urlpatterns = [
    path(f'{API_URL}/auth/', include('apps.users.api.urls')),
    path(f'{API_URL}/customers/', include('apps.customers.api.urls')),
    path(f'{API_URL}/categories/', include('apps.categories.api.urls')),
    path(f'{API_URL}/search/', include('apps.search.api.urls')),
    path('admin/', admin.site.urls),
]
