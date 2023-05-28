from rest_framework.permissions import BasePermission
from rest_framework.request import Request

from other.enums import RoleType


class AdminPermission(BasePermission):
    def has_permission(self, request, view):
        if request.user.role == RoleType.ADMIN:
            return True
        return False


class StaffPermission(BasePermission):
    def has_permission(self, request, view):
        if request.user.role == RoleType.STAFF:
            return True
        return False


class CustomerPermission(BasePermission):
    def has_permission(self, request, view):
        if request.user.role == RoleType.CUSTOMER:
            return True
        return False


class WorkerPermission(BasePermission):
    def has_permission(self, request, view):
        if request.user.role == RoleType.WORKER:
            return True
        return False
