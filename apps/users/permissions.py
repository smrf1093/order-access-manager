from rest_framework.permissions import BasePermission
from .enums import UserRole


class IsAdminOrOwner(BasePermission):

    def has_object_permission(self, request, view, obj):

        if request.user.role == UserRole.ADMIN:
            return True

        return obj.owner == request.user
