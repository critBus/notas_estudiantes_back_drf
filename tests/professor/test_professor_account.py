from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase

from tests.professor.mixin.professor_mixin import ProfessorMixin

User = get_user_model()


class TestProfessorAccount(APITestCase, ProfessorMixin):
    def test_professor_account(self):
        user = User.objects.create_user(
            username="test", email="test@gmail.com", password="123"
        )
        professor = self.create_random_professor(user=user)
        self.assertEqual(user.first_name, professor.first_name)
        self.assertEqual(user.last_name, professor.last_name)

        professor.first_name = "edit1"
        professor.last_name = "edit2"
        professor.save()
        self.assertEqual(user.first_name, professor.first_name)
        self.assertEqual(user.last_name, professor.last_name)

        self.assertTrue(User.objects.filter(id=user.id).exists())
        professor.delete()
        self.assertFalse(User.objects.filter(id=user.id).exists())
