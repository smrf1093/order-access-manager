from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    This level of customization for the user seems
    to be enough,
    the AbstractBaseUser customization is not required
    """
    
    def __str__(self):
        return self.username
