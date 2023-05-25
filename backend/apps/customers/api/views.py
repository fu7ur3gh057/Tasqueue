from rest_framework import permissions, status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.customers.api.serializers import CustomerUpdateSerializer, CustomerSerializer
from apps.customers.exceptions import CustomerNotFound
from apps.customers.models import Customer


# All Views are Authenticated

class CustomerView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CustomerSerializer

    def get(self, request: Request, id: str) -> Response:
        customer = Customer.objects.get(id=id)
        if customer is None:
            raise CustomerNotFound
        serializer = self.serializer_class(customer)
        return Response(serializer.data, status=status.HTTP_200_OK)


class MyCustomerView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CustomerSerializer

    def get(self, request: Request) -> Response:
        customer = request.user.customer
        if customer is None:
            raise CustomerNotFound
        serializer = self.serializer_class(customer)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CustomerUpdateView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CustomerUpdateSerializer

    def put(self, request: Request) -> Response:
        customer = request.user.customer
        if customer is None:
            raise CustomerNotFound
        data = request.data
        serializer = self.serializer_class(instance=customer, data=data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
