from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from django.utils import timezone
from datetime import datetime
from ..models import Order
from apps.users.models import User
from apps.users.enums import UserRole


class AdminOrderTests(APITestCase):
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
            created_at=timezone.make_aware(datetime(2023, 1, 1, 0, 0, 0)),  # Fix here
        )
        self.order2 = Order.objects.create(
            product_name="Product 2",
            quantity=1,
            total_price=50.00,
            created_by=self.customer,
            created_at=timezone.make_aware(datetime(2023, 1, 2, 0, 0, 0)),  # Fix here
        )

        self.client = APIClient()

    def test_admin_cannot_create_order(self):
        """
        Test that an admin cannot create an order.
        """
        self.client.force_authenticate(user=self.admin)
        response = self.client.post(
            reverse("order-list"),  # Use `order-list` for the POST action
            {
                "product_name": "Admin Product",
                "quantity": 1,
                "price": 200.00,
            },
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_can_view_all_orders(self):
        """
        Test that an admin can view all orders.
        """
        self.client.force_authenticate(user=self.admin)
        response = self.client.get(reverse("order-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_admin_can_update_orders(self):
        """
        Test that an admin can update an order.
        """
        self.client.force_authenticate(user=self.admin)
        response = self.client.put(
            reverse("order-detail", args=[self.order1.id]),
            {"product_name": "Admin Updated Product", "quantity": 10},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.order1.refresh_from_db()
        self.assertEqual(self.order1.product_name, "Admin Updated Product")
        self.assertEqual(self.order1.quantity, 10)

    def test_admin_can_delete_orders(self):
        """
        Test that an admin can delete an order.
        """
        self.client.force_authenticate(user=self.admin)
        response = self.client.delete(reverse("order-detail", args=[self.order1.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(Order.objects.filter(id=self.order1.id).exists())

    def test_admin_can_filter_orders(self):
        """
        Test that an admin can filter orders by date range.
        """
        self.client.force_authenticate(user=self.admin)
        response = self.client.get(
            reverse("order-filter"),
            {"start_date": "2023-01-01", "end_date": "2023-12-31"},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
