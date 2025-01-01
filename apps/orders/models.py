from django.db import models
from django.conf import settings
from apps.core.mixins import TimeStampedMixin


class Order(TimeStampedMixin, models.Model):
    product_name = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="orders"
    )

    def __str__(self):
        return f"{self.product_name} - {self.created_by.username}"
