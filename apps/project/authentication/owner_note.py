from rest_framework.permissions import BasePermission
from apps.project.models import StudentNote,Student
from apps.project.models import ROL_NAME_ADMIN

class OwnerNoteOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        return user and (StudentNote.objects.filter(
            student__user=user
        ).exists() or user.groups.filter(id=ROL_NAME_ADMIN).exists())
