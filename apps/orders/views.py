from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.utils.dateparse import parse_datetime
from .models import Order
from apps.users.permissions import get_permission_chain
from apps.users.enums import UserRole
from .serializers import OrderSerializer


class OrderViewSet(ModelViewSet):
    """
    A ViewSet for managing orders.
    """

    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_chain = get_permission_chain()

    def get_queryset(self):
        """
        Customize the queryset based on the user's role.
        - Admins can view all orders.
        - Customers can view only their own orders.
        """
        user = self.request.user
        if not self.permission_chain.handle(self.request, user, "view"):
            return (
                Order.objects.none()
            )  # Return an empty queryset if permission is denied

        if user.role == UserRole.ADMIN:
            return Order.objects.all()  # Admins can view all orders
        return Order.objects.filter(
            created_by=user
        )  # Customers can view their own orders

    def create(self, request, *args, **kwargs):
        """
        Create a new order (Customers only).
        """
        user = request.user
        if not self.permission_chain.handle(request, user, "create"):
            return Response(
                {"error": "Permission denied"}, status=status.HTTP_403_FORBIDDEN
            )

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save(
                created_by=user
            )  # Save the order with the logged-in customer
            return Response(
                {
                    "message": "Order created successfully",
                    "order_id": serializer.data["id"],
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        """
        Update an order (Admins only).
        """
        user = request.user
        if not self.permission_chain.handle(request, user, "update"):
            return Response(
                {"error": "Permission denied"}, status=status.HTTP_403_FORBIDDEN
            )

        try:
            order = self.get_object()
        except Order.DoesNotExist:
            return Response(
                {"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = self.serializer_class(order, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Order updated successfully"}, status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        """
        Delete an order (Admins only).
        """
        user = request.user
        if not self.permission_chain.handle(request, user, "delete"):
            return Response(
                {"error": "Permission denied"}, status=status.HTTP_403_FORBIDDEN
            )

        try:
            order = self.get_object()
        except Order.DoesNotExist:
            return Response(
                {"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND
            )

        order.delete()
        return Response(
            {"message": "Order deleted successfully"}, status=status.HTTP_200_OK
        )

    @action(detail=False, methods=["get"])
    def filter(self, request):
        """
        Filter orders based on date (Admins only).
        """
        user = request.user
        if not self.permission_chain.handle(request, user, "filter"):
            return Response(
                {"error": "Permission denied"}, status=status.HTTP_403_FORBIDDEN
            )

        start_date = parse_datetime(request.query_params.get("start_date"))
        end_date = parse_datetime(request.query_params.get("end_date"))

        if not start_date or not end_date:
            return Response(
                {"error": "Invalid date format"}, status=status.HTTP_400_BAD_REQUEST
            )

        orders = Order.objects.filter(created_at__range=(start_date, end_date))
        serializer = self.serializer_class(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
