from django.urls import path, include

urlpatterns = [
    path("order/", include("apps.orders.urls")),
]
