from django.contrib.auth import get_user_model
from rest_framework import serializers

from apps.users.views.user.serializers.group_serializer import GroupSerializer

User = get_user_model()


class UserRepresentationSerializer(serializers.ModelSerializer):
    groups = GroupSerializer(read_only=True, many=True)

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "is_active",
            "groups",
            "is_superuser",
        ]
