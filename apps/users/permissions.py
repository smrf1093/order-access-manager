from abc import ABC, abstractmethod
from .enums import UserRole


class PermissionHandler(ABC):
    def __init__(self, successor=None):
        self.successor = successor

    @abstractmethod
    def handle(self, request, user, action, *args, **kwargs):
        pass


class AdminPermissionHandler(PermissionHandler):
    def handle(self, request, user, action, *args, **kwargs):
        if user.role == UserRole.ADMIN.value:
            if action in ["view", "update", "delete", "filter"]:
                return True
        elif self.successor:
            return self.successor.handle(request, user, action, *args, **kwargs)
        return False


class CustomerPermissionHandler(PermissionHandler):
    def handle(self, request, user, action, *args, **kwargs):
        if user.role == UserRole.CUSTOMER.value:
            if action in ["create", "view"]:
                return True
        elif self.successor:
            return self.successor.handle(request, user, action, *args, **kwargs)
        return False


class DefaultPermissionHandler(PermissionHandler):
    def handle(self, request, user, action, *args, **kwargs):
        return False


def get_permission_chain():
    return AdminPermissionHandler(CustomerPermissionHandler(DefaultPermissionHandler()))
