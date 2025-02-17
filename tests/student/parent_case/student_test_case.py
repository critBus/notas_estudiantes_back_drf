from datetime import timedelta

from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework.test import APITestCase

from apps.project.models import SchoolYear
from tests.student.mixin.subject_mixin import SubjectMixin
from tests.utils.mixin.api_crud_mixin import ApiCrudMixin
from tests.utils.mixin.user_mixin import UserMixin

User = get_user_model()


class StudentTestCase(APITestCase, ApiCrudMixin, UserMixin, SubjectMixin):
    def setUp(self) -> None:
        SchoolYear.objects.create(
            name="2025-2026",
            start_date=timezone.now().date(),
            end_date=(timezone.now() + timedelta(days=365)).date(),
        )
        self.login_superuser()
        self.crear_asignaturas()
