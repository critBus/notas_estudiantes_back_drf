import json
from typing import Optional, TypeVar

from django.conf import settings
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status

User = get_user_model()

T = TypeVar("T")


class UserMixin:
    def get_admin_data(self):
        return {
            "id": 1,
            "username": settings.DJANGO_SUPERUSER_USERNAME,
            "email": settings.DJANGO_SUPERUSER_EMAIL,
            "first_name": settings.DJANGO_SUPERUSER_FIRST_NAME,
            "last_name": settings.DJANGO_SUPERUSER_LAST_NAME,
            "groups": [{"id": 1, "name": "admin"}],
            "is_active": True,
            "is_superuser": True,
        }

    def login_superuser(self):
        self.login(
            username=settings.DJANGO_SUPERUSER_USERNAME,
            password=settings.DJANGO_SUPERUSER_PASSWORD,
        )
        self.put_authentication_in_the_header()

    def login(
        self,
        username: str,
        password: Optional[str],
        unauthorized: bool = False,
        print_json_response: bool = False,
    ):
        URL = reverse("token_obtain_pair")
        # print(f"loguin {URL}")
        payload = {
            "username": username,
            "password": password,
        }
        response = self.client.post(URL, payload)
        if print_json_response:
            response_dict = json.loads(str(response.content, encoding="utf8"))
            pretty = json.dumps(response_dict, indent=4)
            print(pretty)
        if unauthorized:
            self.assertEqual(
                response.status_code,
                status.HTTP_401_UNAUTHORIZED,
            )
            return
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_dict = json.loads(str(response.content, encoding="utf8"))
        self.assertEqual(True, "access" in response_dict)
        self.assertEqual(True, "refresh" in response_dict)
        self.access_token = response_dict["access"]
        self.refresh_token = response_dict["refresh"]

    def put_authentication_in_the_header(
        self, access_token: Optional[str] = None
    ):
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.access_token if not access_token else access_token}"
        )

    def clear_authentication_in_the_header(self):
        self.client.credentials(HTTP_AUTHORIZATION="")
        self.client.logout()
