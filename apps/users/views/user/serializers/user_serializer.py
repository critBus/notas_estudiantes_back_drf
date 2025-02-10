from django.contrib.auth import get_user_model
from rest_framework import serializers

from apps.users.views.user.serializers.group_serializer import GroupSerializer

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    groups = GroupSerializer(read_only=True, many=True)

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "password",
            "groups",
            "is_active",
        ]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            if attr == "password":
                instance.set_password(value)
            else:
                setattr(instance, attr, value)
        instance.save()
        return instance
