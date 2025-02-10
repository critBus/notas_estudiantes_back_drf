from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework.test import APITestCase

from apps.users.views.user.serializers.user_serializer import UserSerializer

User = get_user_model()


class UserSerializerTests(APITestCase):
    def setUp(self):
        # Crea algunos grupos para usar en los tests
        self.group1 = Group.objects.create(name="group1")
        self.group2 = Group.objects.create(name="group2")
        self.group3 = Group.objects.create(name="group3")

    def test_create_user_with_valid_groups(self):
        data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "password123",
            "groups": ["group1", "group2"],
        }
        serializer = UserSerializer(data=data)
        self.assertTrue(serializer.is_valid())

        user = serializer.save()

        self.assertEqual(user.groups.count(), 2)
        self.assertIn(self.group1, user.groups.all())
        self.assertIn(self.group2, user.groups.all())

    def test_create_user_with_invalid_group(self):
        data = {
            "username": "testuser2",
            "email": "test2@example.com",
            "password": "password123",
            "groups": ["group1", "nonexistent_group"],
        }
        serializer = UserSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn(
            "Los siguientes grupos no existen: nonexistent_group",
            serializer.errors["groups"][0],
        )

    def test_create_user_with_no_groups(self):
        data = {
            "username": "testuser3",
            "email": "test3@example.com",
            "password": "password123",
        }
        serializer = UserSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        user = serializer.save()
        self.assertEqual(user.groups.count(), 0)

    def test_update_user_add_groups(self):
        user = User.objects.create_user(
            username="testuser4", password="password123"
        )  # Crear usuario sin grupos.
        data = {
            "groups": ["group1", "group3"],
        }
        serializer = UserSerializer(
            instance=user, data=data, partial=True
        )  # partial=True para permitir update parcial
        self.assertTrue(serializer.is_valid())
        user = serializer.save()
        self.assertEqual(user.groups.count(), 2)
        self.assertIn(self.group1, user.groups.all())
        self.assertIn(self.group3, user.groups.all())

    def test_update_user_remove_all_groups(self):
        user = User.objects.create_user(
            username="testuser5", password="password123"
        )
        user.groups.add(self.group1)  # Añade un grupo inicialmente
        user.groups.add(self.group2)
        data = {
            "groups": [],  # Lista vacía para eliminar todos los grupos
        }
        serializer = UserSerializer(instance=user, data=data, partial=True)
        self.assertTrue(serializer.is_valid())
        user = serializer.save()
        self.assertEqual(user.groups.count(), 0)

    def test_update_user_with_no_groups_in_data(self):
        user = User.objects.create_user(
            username="testuser6", password="password123"
        )
        user.groups.add(self.group1)  # Añade un grupo inicialmente
        data = {
            "email": "new_email@example.com",  # Actualiza solo el email
        }
        serializer = UserSerializer(instance=user, data=data, partial=True)
        self.assertTrue(serializer.is_valid())
        user = serializer.save()
        self.assertEqual(
            user.email, "new_email@example.com"
        )  # Comprueba que se actualizo el email.
        self.assertEqual(
            user.groups.count(), 1
        )  # No debe haber cambiado los grupos.
        self.assertIn(
            self.group1, user.groups.all()
        )  # Debe mantener el grupo anterior.

    def test_update_user_with_invalid_group(self):
        user = User.objects.create_user(
            username="testuser7", password="password123"
        )
        data = {
            "groups": ["group1", "nonexistent_group"],
        }
        serializer = UserSerializer(instance=user, data=data, partial=True)
        self.assertFalse(serializer.is_valid())
        self.assertIn(
            "Los siguientes grupos no existen: nonexistent_group",
            serializer.errors["groups"][0],
        )
