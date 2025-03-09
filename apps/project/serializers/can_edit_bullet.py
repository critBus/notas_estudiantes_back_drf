from rest_framework import serializers


class CanEditBulletSerializer(serializers.Serializer):
    can_edit_bullet = serializers.BooleanField()
