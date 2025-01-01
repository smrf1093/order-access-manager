from django.test import TestCase
from apps.users.models import User, UserRole


class UserModelTestCase(TestCase):
    def test_create_regular_user(self):
        """
        Test creating a regular user with the default role.
        """
        user = User.objects.create_user(
            username="regular_user", email="regular@example.com", password="password123"
        )
        self.assertEqual(user.username, "regular_user")
        self.assertEqual(user.email, "regular@example.com")
        self.assertTrue(user.check_password("password123"))
        self.assertEqual(user.role, UserRole.CUSTOMER.value)

    def test_create_admin_user(self):
        """
        Test creating an admin user.
        """
        admin_user = User.objects.create_superuser(
            username="admin_user",
            email="admin@example.com",
            password="adminpassword123",
        )
        self.assertEqual(admin_user.username, "admin_user")
        self.assertEqual(admin_user.email, "admin@example.com")
        self.assertTrue(admin_user.check_password("adminpassword123"))
        self.assertEqual(admin_user.role, UserRole.ADMIN.value)

    def test_user_string_representation(self):
        """
        Test the string representation of the user.
        """
        user = User.objects.create_user(
            username="test_user", email="test@example.com", password="password123"
        )
        self.assertEqual(str(user), "test_user")
