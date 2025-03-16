from rest_framework import serializers


class WithoutGrantingSerializer(serializers.Serializer):
    without_granting = serializers.BooleanField()
