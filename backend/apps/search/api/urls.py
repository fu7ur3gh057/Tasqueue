# search/urls.py
from django.urls import path
from apps.search.api.views import SearchCustomersView

urlpatterns = [
    path('customers/<str:query>/', SearchCustomersView.as_view()),
]
