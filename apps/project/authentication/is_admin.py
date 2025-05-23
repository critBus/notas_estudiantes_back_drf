from rest_framework.permissions import BasePermission
from apps.project.models import ROL_NAME_ADMIN
class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        user=request.user
        return user and user.groups.filter(id=ROL_NAME_ADMIN).exists()