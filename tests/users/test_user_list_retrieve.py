import json

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from ..utils.mixin.user_mixin import UserMixin

User = get_user_model()


class UserViewSetTests(APITestCase, UserMixin):
    def setUp(self):
        self.group1 = Group.objects.create(name="group1")
        self.group2 = Group.objects.create(name="group2")
        self.user_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "password123",
        }
        self.login_superuser()  # Asegurarse de que el usuario 'admin' existe (o crearlo si no) y tiene ID 1
        self.maxDiff = None

        # self.admin_user = User.objects.get(username='admin')
        # # try:
        # # except User.DoesNotExist:
        # #     self.admin_user = User.objects.create_superuser(username='admin', email='admin@gmail.dev', password='password123')
        # #     self.admin_user.first_name = 'admin'
        # #     self.admin_user.last_name = 'admin'
        # #     self.admin_user.save()
        # self.assertEqual(self.admin_user.id, 1)

    def assertDictContainsSubset(self, subset, dictionary):
        """Versión mejorada de assertDictContainsSubset que maneja listas."""
        for key, value in subset.items():
            if isinstance(value, list):  # Si el valor es una lista
                self.assertEqual(
                    len(value), len(dictionary[key])
                )  # Compara longitudes
                for i, item in enumerate(value):
                    if isinstance(
                        item, dict
                    ):  # Si el elemento de la lista es un diccionario
                        self.assertDictContainsSubset(
                            item, dictionary[key][i]
                        )  # Recursión
                    else:
                        self.assertEqual(
                            item, dictionary[key][i]
                        )  # Compara elementos de la lista
            elif isinstance(value, dict):  # Si es un diccionario
                self.assertDictContainsSubset(
                    value, dictionary[key]
                )  # Recursión
            else:
                self.assertEqual(
                    value, dictionary[key]
                )  # Compara valores directamente

    def test_list_users(self):
        data_user_1 = {
            "username": "testuser1",
            "email": "test1@example.com",
            "password": "password123",
            "first_name": "first_name1",
            "last_name": "last_name1",
        }
        user1 = User.objects.create_user(**data_user_1)
        user1.groups.add(self.group1)

        data_user_2 = {
            "username": "testuser2",
            "email": "test2@example.com",
            "password": "password123",
            "first_name": "first_name2",
            "last_name": "last_name2",
        }
        user2 = User.objects.create_user(**data_user_2)
        user2.groups.add(self.group2)

        url = reverse("user-list")
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data_user_1.pop("password")
        data_user_2.pop("password")
        expected_data = {
            "count": 3,
            "next": None,
            "previous": None,
            "results": [
                self.get_admin_data(),
                {
                    "id": user1.id,
                    "is_active": True,
                    "groups": [
                        {"id": self.group1.id, "name": self.group1.name}
                    ],
                    "is_superuser": False,
                    **data_user_1,
                },
                {
                    "id": user2.id,
                    "is_active": True,
                    "groups": [
                        {"id": self.group2.id, "name": self.group2.name}
                    ],
                    "is_superuser": False,
                    **data_user_2,
                },
            ],
        }
        response_dict = json.loads(str(response.content, encoding="utf8"))
        self.assertDictEqual(expected_data, response_dict)

    def test_retrieve_user(self):
        data_user_1 = {
            "username": "testuser1",
            "email": "test1@example.com",
            "password": "password123",
            "first_name": "first_name1",
            "last_name": "last_name1",
        }
        user = User.objects.create_user(**data_user_1)
        user.groups.add(self.group1)

        url = reverse("user-detail", kwargs={"pk": user.pk})
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data_user_1.pop("password")
        expected_data = {
            "id": user.id,
            "is_active": True,
            "groups": [{"id": self.group1.id, "name": self.group1.name}],
            "is_superuser": False,
            **data_user_1,
        }
        response_dict = json.loads(str(response.content, encoding="utf8"))
        self.assertDictEqual(expected_data, response_dict)

        # Prueba con el usuario admin
        url = reverse("user-detail", kwargs={"pk": 1})
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertDictContainsSubset(self.get_admin_data(), response.data)
