from django.contrib.auth import get_user_model
from rest_framework import serializers

from apps.users.views.user.serializers.user_serializer import UserSerializer

User = get_user_model()


class AuthenticationResponseSerializer(serializers.Serializer):
    user = UserSerializer()
    status = serializers.ChoiceField(choices=["success"])
    access = serializers.CharField(allow_blank=False)
    refresh = serializers.CharField(allow_blank=False)
