import datetime

from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


def dentro_de_10_minutos(date):
    ahora = datetime.datetime.now()
    diff = ahora.replace(tzinfo=None) - date.replace(tzinfo=None)
    return diff.total_seconds() < 600


class CredentialsSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    date = serializers.DateTimeField()

    def validate_username(self, username):
        # print(f"username {username}")
        self.user = User.objects.filter(username=username).first()
        if not self.user:
            raise serializers.ValidationError("No existe este username ")
        return username

    # def validate_password(self, password):
    #     if not self.user.check_password(password):
    #         raise serializers.ValidationError("Contraseña Incorrecta")
    #     return password
    def validate_date(self, date):
        if not dentro_de_10_minutos(date):
            raise serializers.ValidationError("Las credenciales ya vencieron")
        return date

    def validate(self, validated_data):
        password = validated_data.get("password")
        if (not self.user) or not self.user.check_password(password):
            raise serializers.ValidationError("Contraseña Incorrecta")
        return validated_data
