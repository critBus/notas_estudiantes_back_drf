from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase

from apps.project.management.commands.init_data import (
    creat_first_superuser_and_roles,
)
from tests.student.mixin.school_year_mixin import SchoolYearMixin
from tests.student.mixin.subject_mixin import SubjectMixin
from tests.utils.mixin.api_crud_mixin import ApiCrudMixin
from tests.utils.mixin.user_mixin import UserMixin

User = get_user_model()


class StudentTestCase(
    APITestCase, ApiCrudMixin, UserMixin, SubjectMixin, SchoolYearMixin
):
    def setUp(self) -> None:
        creat_first_superuser_and_roles()
        self.create_current_school_year()
        self.login_superuser()
        self.crear_asignaturas()
        self.maxDiff = None
