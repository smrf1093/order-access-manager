from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from django.utils import timezone
from datetime import datetime
from ..models import Order
from apps.users.models import User
from apps.users.enums import UserRole


class CustomerOrderTests(APITestCase):

    def setUp(self):
        self.customer = User.objects.create_user(
            username="customer1",
            email="customer1@example.com",
            password="customerpassword",
            role=UserRole.CUSTOMER,
        )

        self.admin = User.objects.create_user(
            username="admin1",
            email="admin1@example.com",
            password="adminpassword",
            role=UserRole.ADMIN,
        )

        self.order1 = Order.objects.create(
            product_name="Product 1",
            quantity=2,
            total_price=100.00,
            created_by=self.customer,
            created_at=timezone.make_aware(datetime(2023, 1, 1, 0, 0, 0)),
        )
        self.order2 = Order.objects.create(
            product_name="Product 2",
            quantity=1,
            total_price=50.00,
            created_by=self.customer,
            created_at=timezone.make_aware(datetime(2023, 1, 2, 0, 0, 0)),
        )

        self.client = APIClient()

    def test_customer_can_create_order(self):
        """
        Test that a customer can create a new order.
        """
        self.client.force_authenticate(user=self.customer)
        response = self.client.post(
            reverse("order-list"),
            {
                "product_name": "New Product",
                "quantity": 3,
                "total_price": 150.00,
            },
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Order.objects.filter(created_by=self.customer).count(), 3)

    def test_customer_can_view_own_orders(self):
        """
        Test that a customer can view their own orders.
        """
        self.client.force_authenticate(user=self.customer)
        response = self.client.get(reverse("order-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_customer_cannot_update_orders(self):
        """
        Test that a customer cannot update orders.
        """
        self.client.force_authenticate(user=self.customer)
        response = self.client.put(
            reverse("order-detail", args=[self.order1.id]),
            {"product_name": "Updated Product", "quantity": 5},
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_customer_cannot_delete_orders(self):
        """
        Test that a customer cannot delete orders.
        """
        self.client.force_authenticate(user=self.customer)
        response = self.client.delete(reverse("order-detail", args=[self.order1.id]))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_customer_cannot_filter_orders(self):
        """
        Test that a customer cannot filter orders.
        """
        self.client.force_authenticate(user=self.customer)
        response = self.client.get(
            reverse("order-filter"),
            {"start_date": "2023-01-01", "end_date": "2023-12-31"},
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
