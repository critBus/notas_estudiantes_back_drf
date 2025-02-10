from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework import status
from rest_framework.reverse import reverse  # Para generar urls
from rest_framework.test import APITestCase

from tests.utils.mixin.user_mixin import UserMixin

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
        self.login_superuser()

    def tearDown(self):
        super().tearDown()
        User.objects.all().delete()

    def test_create_user_with_valid_groups(self):
        data = self.user_data.copy()
        data["groups"] = ["group1", "group2"]
        url = reverse("user-list")  # Obtener la url de la lista de usuarios
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        user = User.objects.get(username=data["username"])
        self.assertEqual(user.groups.count(), 2)
        self.assertIn(self.group1, user.groups.all())
        self.assertIn(self.group2, user.groups.all())

        # Verifica la representación del JSON
        expected_data = {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "first_name": "",  # Valores por defecto
            "last_name": "",
            "groups": [
                {"id": self.group1.id, "name": "group1"},
                {"id": self.group2.id, "name": "group2"},
            ],
            "is_superuser": False,
            "is_active": True,
        }
        # pretty = json.dumps(response.data, indent=4)
        # print(pretty)
        self.assertEqual(response.data, expected_data)

    def test_create_user_with_invalid_group(self):
        data = self.user_data.copy()
        data["groups"] = ["group1", "nonexistent_group"]
        url = reverse("user-list")
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(
            "Los siguientes grupos no existen: nonexistent_group",
            response.data["groups"][0],
        )

    def test_create_user_with_no_groups(self):
        data = self.user_data.copy()
        url = reverse("user-list")
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = User.objects.get(username=data["username"])
        self.assertEqual(user.groups.count(), 0)

        expected_data = {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "first_name": "",
            "last_name": "",
            "groups": [],
            "is_superuser": False,
            "is_active": True,
        }
        self.assertEqual(response.data, expected_data)

    def test_update_user_add_groups(self):
        user = User.objects.create_user(**self.user_data)
        url = reverse(
            "user-detail", kwargs={"pk": user.pk}
        )  # Obtener la url del detalle de usuario
        data = {"groups": ["group1", "group2"]}
        response = self.client.patch(
            url, data, format="json"
        )  # Usar PATCH para actualizaciones parciales
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user.refresh_from_db()  # Recargar el usuario desde la base de datos
        self.assertEqual(user.groups.count(), 2)
        self.assertIn(self.group1, user.groups.all())
        self.assertIn(self.group2, user.groups.all())
        expected_data = {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "first_name": "",
            "last_name": "",
            "groups": [
                {"id": self.group1.id, "name": "group1"},
                {"id": self.group2.id, "name": "group2"},
            ],
            "is_superuser": False,
            "is_active": True,
        }
        self.assertEqual(response.data, expected_data)

    def test_update_user_remove_all_groups(self):
        user = User.objects.create_user(**self.user_data)
        user.groups.add(self.group1)
        user.groups.add(self.group2)
        url = reverse("user-detail", kwargs={"pk": user.pk})
        data = {"groups": []}
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user.refresh_from_db()
        self.assertEqual(user.groups.count(), 0)
        expected_data = {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "first_name": "",
            "last_name": "",
            "groups": [],
            "is_superuser": False,
            "is_active": True,
        }
        self.assertEqual(response.data, expected_data)

    def test_update_user_with_no_groups_in_data(self):
        user = User.objects.create_user(**self.user_data)
        user.groups.add(self.group1)
        url = reverse("user-detail", kwargs={"pk": user.pk})
        data = {"email": "new_email@example.com"}
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user.refresh_from_db()
        self.assertEqual(user.email, "new_email@example.com")
        self.assertEqual(user.groups.count(), 1)
        self.assertIn(self.group1, user.groups.all())
        expected_data = {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "first_name": "",
            "last_name": "",
            "groups": [{"id": self.group1.id, "name": "group1"}],
            "is_superuser": False,
            "is_active": True,
        }
        self.assertEqual(response.data, expected_data)

    def test_update_user_with_invalid_group(self):
        user = User.objects.create_user(**self.user_data)
        url = reverse("user-detail", kwargs={"pk": user.pk})
        data = {"groups": ["group1", "nonexistent_group"]}
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(
            "Los siguientes grupos no existen: nonexistent_group",
            response.data["groups"][0],
        )
