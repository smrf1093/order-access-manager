from django.db import models


class UserRole(models.TextChoices):
    ADMIN = "ADMIN", "Admin"
    USER = "USER", "User"
