from django.urls import path
from apps.workers.api.views import WorkerView, WorkerUpdateView, MyWorkerView

urlpatterns = [
    path("update/", WorkerView.as_view(), name='update'),
    path('', MyWorkerView.as_view()),
    path('<id>/', WorkerView.as_view()),
]
