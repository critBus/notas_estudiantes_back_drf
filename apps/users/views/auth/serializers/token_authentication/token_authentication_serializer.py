import json
import traceback

from django.conf import settings
from rest_framework import serializers

from config.utils.utils_logs import logger
from config.utils.utils_rsa import desencriptar_rsa

from .credentials_serializer import CredentialsSerializer


class TokenAuthenticationSerializer(serializers.Serializer):
    credentials = serializers.CharField()

    def validate_credentials(self, credentials):
        try:
            data_json = desencriptar_rsa(
                private_key_str=settings.PRIVATE_KEY_BACKUP_API,
                mensaje_cifrado_str=credentials,
            )
            data = json.loads(data_json)
            serializador = CredentialsSerializer(data=data)
            if serializador.is_valid():
                self.user = serializador.user
                return credentials

            # print(serializador.errors)

        except:
            logger.error(traceback.format_exc())
        raise serializers.ValidationError("Credenciales invalidas")
