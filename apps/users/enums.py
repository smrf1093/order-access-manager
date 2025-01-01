from django.db import models


class UserRole(models.TextChoices):
    ADMIN = "ADMIN", "Admin"
    CUSTOMER = "CUSTOMER", "Customer"
