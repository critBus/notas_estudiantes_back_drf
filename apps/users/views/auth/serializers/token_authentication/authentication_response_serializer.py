
from django.contrib.auth import get_user_model
from rest_framework import serializers

from apps.users.views.user.serializers.user_representation_serializer import (
    UserRepresentationSerializer,
)

User = get_user_model()


class AuthenticationResponseSerializer(serializers.Serializer):
    user = UserRepresentationSerializer()
    status = serializers.ChoiceField(choices=["success"])
    access = serializers.CharField(allow_blank=False)
    refresh = serializers.CharField(allow_blank=False)
