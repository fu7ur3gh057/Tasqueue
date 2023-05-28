from django.urls import path
from .views import *

urlpatterns = [
    path('', ServiceListView.as_view(), name='list'),
    path('tree/', ServiceTreeView.as_view(), name='tree'),
    path('<service_id>/', ServiceView.as_view(), name='by_id'),
]
