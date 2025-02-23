from typing import Dict, Optional

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework.reverse import reverse  # Para generar urls

from apps.project.models import ROL_NAME_STUDENT, Student
from tests.student.parent_case.student_test_case import StudentTestCase

User = get_user_model()


class TestCreateStudent(StudentTestCase):
    def call_create_student(
        self,
        ci: str,
        address: str,
        grade: str,
        last_name: str,
        first_name: str,
        registration_number: str,
        sex: str,
        account: Optional[Dict[str, str]] = None,
        unauthorized: bool = False,
        forbidden: bool = False,
        bad_request: bool = False,
        print_json_response: bool = False,
    ):
        URL = reverse("students-list")

        payload = {
            "ci": ci,
            "address": address,
            "grade": grade,
            "last_name": last_name,
            "first_name": first_name,
            "registration_number": registration_number,
            "sex": sex,
        }
        if account:
            payload["account"] = account

        return self.call_create(
            url=URL,
            payload=payload,
            unauthorized=unauthorized,
            forbidden=forbidden,
            bad_request=bad_request,
            print_json_response=print_json_response,
            format_json=True,
        )

    def test_add_student(self):
        data = {
            "ci": "123214",
            "address": "address",
            "grade": 7,
            "last_name": "last_name",
            "first_name": "test_student",
            "registration_number": "str123213ing",
            "sex": "F",
        }
        response_dict = self.call_create_student(**data)
        id = self.assertKey(
            response_dict=response_dict, key="id", expected_type=int
        )
        student = Student.objects.filter(id=id).first()
        self.assertIsNotNone(student)
        self.assertIsNone(student.user)

    def test_add_student_account(self):
        data = {
            "ci": "123214",
            "address": "address",
            "grade": 7,
            "last_name": "last_name",
            "first_name": "test_student",
            "registration_number": "str123213ing",
            "sex": "F",
            "account": {
                "username": "student",
                "password": "studentpassword",
                "email": "student@example.com",
            },
        }
        response_dict = self.call_create_student(**data)
        id = self.assertKey(
            response_dict=response_dict, key="id", expected_type=int
        )
        student = Student.objects.filter(id=id).first()
        self.assertIsNotNone(student)
        self.assertIsNotNone(student.user)

        self.assertEqual(student.user.username, data["account"]["username"])
        self.assertEqual(student.user.email, data["account"]["email"])
        student.user.check_password(data["account"]["password"])
        self.assertTrue(
            Group.objects.filter(
                user=student.user, name=ROL_NAME_STUDENT
            ).exists()
        )

        data = {
            "ci": "12321232114",
            "address": "address2",
            "grade": 7,
            "last_name": "last_name2",
            "first_name": "test_student2",
            "registration_number": "str123213213213ing",
            "sex": "F",
            "account": {
                "username": "student",
                "password": "studentpassword",
                "email": "student@example.com",
            },
        }
        self.call_create_student(
            **data, bad_request=True, print_json_response=False
        )
