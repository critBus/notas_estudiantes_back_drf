from django.contrib.auth.models import Group

from apps.users.views.user.serializers.group_serializer import GroupSerializer
from config.utils.utils_view import BaseModelViewSet


class GroupViewSet(BaseModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
