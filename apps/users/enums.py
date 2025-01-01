from django.db import models


class UserRole(models.TextChoices):
    ADMIN = "admin", "Admin"
    USER = "user", "User"
