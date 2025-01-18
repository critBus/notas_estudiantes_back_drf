from rest_framework import serializers


class TokenAccesBlacklistSerializer(serializers.Serializer):
    refresh = serializers.CharField(allow_blank=False)
