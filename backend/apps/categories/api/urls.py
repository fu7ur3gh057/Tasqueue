from django.urls import path
from .views import *

urlpatterns = [
    path('', CategoryListView.as_view(), name='list'),
    path('tree/', CategoryTreeView.as_view(), name='tree'),
    path('<service_id>/', CategoryView.as_view(), name='by_id'),
]
