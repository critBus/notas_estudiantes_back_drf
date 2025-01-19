from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class CredentialsSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate_username(self, username):
        # print(f"username {username}")
        self.user = User.objects.filter(username=username).first()
        if not self.user:
            raise serializers.ValidationError("No existe este username ")
        return username

    def validate(self, validated_data):
        password = validated_data.get("password")
        if (not self.user) or not self.user.check_password(password):
            raise serializers.ValidationError("Contraseña Incorrecta")
        return validated_data
