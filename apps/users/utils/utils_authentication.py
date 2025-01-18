import json
from datetime import datetime

from django.conf import settings

from config.utils.utils_rsa import encriptar_rsa


def get_credentials_rsa(username, password):
    # [root]
    json_str = json.dumps(
        {
            "username": username,
            "password": password,
            "date": datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f%z"),
        }
    )
    return encriptar_rsa(
        public_key_str=settings.PUBLIC_KEY_BACKUP_API, mensaje=json_str
    )
