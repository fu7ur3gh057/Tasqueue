from django.urls import path
from apps.customers.api.views import CustomerView, MyCustomerView, CustomerUpdateView

urlpatterns = [
    path("update/", CustomerUpdateView.as_view(), name='update'),
    path('', MyCustomerView.as_view()),
    path('<id>/', CustomerView.as_view()),
]
