from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.project.management.commands.init_data import (
    creat_first_superuser_and_roles,
)
from apps.project.models import SchoolYear
from tests.utils.mixin.user_mixin import UserMixin


class SchoolYearTests(APITestCase, UserMixin):
    def setUp(self):
        super().setUp()
        creat_first_superuser_and_roles()
        self.login_superuser()

    def test_create_school_year_with_valid_dates(self):
        """
        Test para asegurarse de que se puede crear un SchoolYear con fechas válidas.
        """
        url = reverse(
            "school_year-list"
        )  # Asegúrate de que 'schoolyear-list' sea el nombre correcto de tu URL
        data = {
            "start_date": "2024-09-01",
            "end_date": "2025-06-30",
            "name": "2024-2025",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(SchoolYear.objects.count(), 1)
        self.assertEqual(SchoolYear.objects.get().name, "2024-2025")

    def test_create_school_year_with_invalid_dates(self):
        """
        Test para asegurarse de que no se puede crear un SchoolYear con fechas inválidas.
        """
        url = reverse(
            "school_year-list"
        )  # Asegúrate de que 'schoolyear-list' sea el nombre correcto de tu URL
        data = {
            "start_date": "2025-06-30",
            "end_date": "2024-09-01",
            "name": "2024-2025",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(SchoolYear.objects.count(), 0)
