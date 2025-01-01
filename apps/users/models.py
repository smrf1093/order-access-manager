from django.contrib.auth.models import AbstractUser
from django.db import models
from .enums import UserRole
from .managers import UserManager


class User(AbstractUser):
    """
    This level of customization for the user seems
    to be enough,
    the AbstractBaseUser customization is not required
    """

    role = models.CharField(
        max_length=10, choices=UserRole.choices, default=UserRole.CUSTOMER
    )

    objects = UserManager()

    def __str__(self):
        return self.username
