from rest_framework import permissions, status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.services.exceptions import ServiceNotFound
from apps.services.models import Service
from apps.users.models import User
from apps.users.permissions import WorkerPermission
from apps.workers.api.serializers import WorkerSerializer, WorkerUpdateSerializer


class WorkerView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = WorkerSerializer

    def get(self, request: Request, id: str) -> Response:
        customer = Service.objects.get(id=id)
        if customer is None:
            raise ServiceNotFound
        serializer = self.serializer_class(customer)
        return Response(serializer.data, status=status.HTTP_200_OK)


class MyWorkerView(APIView):
    permission_classes = [permissions.IsAuthenticated, WorkerPermission]
    serializer_class = WorkerSerializer

    def get(self, request: Request) -> Response:
        worker = request.user.worker
        if worker is None:
            raise ServiceNotFound
        serializer = self.serializer_class(worker)
        return Response(serializer.data, status=status.HTTP_200_OK)


class WorkerUpdateView(APIView):
    permission_classes = [permissions.IsAuthenticated, WorkerPermission]
    serializer_class = WorkerUpdateSerializer

    def put(self, request: Request) -> Response:
        pass
