from django.contrib.auth.models import Group
from rest_framework import status
from rest_framework.test import APITestCase

from apps.project.management.commands.init_data import (
    creat_first_superuser_and_roles,
)
from tests.utils.mixin.user_mixin import UserMixin

API_CRUD_GROUP = "/api/groups/"

INITIAL_AMOUNT = 4


class GroupTests(APITestCase, UserMixin):
    def setUp(self):
        creat_first_superuser_and_roles()
        # Crear algunos grupos de prueba
        self.group1 = Group.objects.create(name="Admin")
        self.group2 = Group.objects.create(name="Editor")
        self.group3 = Group.objects.create(name="Viewer")
        self.login_superuser()

    def tearDown(self):
        super().tearDown()
        Group.objects.all().delete()

    def test_list_groups(self):
        """
        Prueba que se puedan listar todos los grupos.
        """
        response = self.client.get(API_CRUD_GROUP)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("results", response.data)
        roles_data = response.data["results"]
        self.assertEqual(
            len(roles_data), 3 + INITIAL_AMOUNT
        )  # Verifica que se devuelvan 3 grupos
        self.assertEqual(roles_data[0 + INITIAL_AMOUNT]["name"], "Admin")
        self.assertEqual(roles_data[1 + INITIAL_AMOUNT]["name"], "Editor")
        self.assertEqual(roles_data[2 + INITIAL_AMOUNT]["name"], "Viewer")

    def test_retrieve_group(self):
        """
        Prueba que se pueda recuperar un grupo específico por su ID.
        """
        response = self.client.get(f"{API_CRUD_GROUP}{self.group1.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Admin")

    def test_create_group(self):
        """
        Prueba que se pueda crear un nuevo grupo.
        """
        data = {"name": "Manager"}
        response = self.client.post(API_CRUD_GROUP, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            Group.objects.count(), 4 + INITIAL_AMOUNT
        )  # Verifica que se haya creado un nuevo grupo
        self.assertEqual(
            Group.objects.get(id=response.data["id"]).name, "Manager"
        )

    def test_update_group(self):
        """
        Prueba que se pueda actualizar un grupo existente.
        """
        data = {"name": "SuperAdmin"}
        response = self.client.put(
            f"{API_CRUD_GROUP}{self.group1.id}/", data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.group1.refresh_from_db()  # Actualiza la instancia desde la base de datos
        self.assertEqual(self.group1.name, "SuperAdmin")

    def test_partial_update_group(self):
        """
        Prueba que se pueda actualizar parcialmente un grupo existente.
        """
        data = {"name": "SuperEditor"}
        response = self.client.patch(
            f"{API_CRUD_GROUP}{self.group2.id}/", data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.group2.refresh_from_db()  # Actualiza la instancia desde la base de datos
        self.assertEqual(self.group2.name, "SuperEditor")

    def test_delete_group(self):
        """
        Prueba que se pueda eliminar un grupo existente.
        """
        response = self.client.delete(f"{API_CRUD_GROUP}{self.group3.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(
            Group.objects.count(), 2 + INITIAL_AMOUNT
        )  # Verifica que se haya eliminado un grupo
        self.assertFalse(
            Group.objects.filter(id=self.group3.id).exists()
        )  # Verifica que el grupo ya no existe
