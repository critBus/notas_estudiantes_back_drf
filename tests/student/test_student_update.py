from typing import Dict, Optional

from django.contrib.auth import get_user_model
from rest_framework.reverse import reverse  # Para generar urls

from apps.project.models import Student
from tests.student.parent_case.student_test_case import StudentTestCase

User = get_user_model()


class TestUpdateStudent(StudentTestCase):
    def call_update_student(
        self,
        entity_id: int,
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
        URL = reverse("students-detail", args=[entity_id])

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

        return self.call_update(
            url=URL,
            payload=payload,
            unauthorized=unauthorized,
            forbidden=forbidden,
            bad_request=bad_request,
            print_json_response=print_json_response,
            format_json=True,
        )

    def test_update_student(self):
        student = self.create_random_student()
        data = {
            "ci": "123214",
            "address": "address",
            "grade": 7,
            "last_name": "last_name",
            "first_name": "test_student",
            "registration_number": "str123213ing",
            "sex": "F",
        }
        response_dict = self.call_update_student(
            **data, entity_id=student.id, print_json_response=False
        )

        id = self.assertKey(
            response_dict=response_dict, key="id", expected_type=int
        )
        student = Student.objects.filter(id=id).first()
        self.assertIsNotNone(student)
        self.assertIsNone(student.user)

    def test_update_student_account(self):
        student = self.create_random_student()
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
        response_dict = self.call_update_student(**data, entity_id=student.id)
        id = self.assertKey(
            response_dict=response_dict, key="id", expected_type=int
        )
        student = Student.objects.filter(id=id).first()
        self.assertIsNotNone(student)
        user = student.user
        self.assertIsNotNone(user)
        self.assertEqual(student.user.username, data["account"]["username"])
        self.assertEqual(student.user.email, data["account"]["email"])
        student.user.check_password(data["account"]["password"])

        data = {
            "ci": "123214",
            "address": "address",
            "grade": 7,
            "last_name": "last_name",
            "first_name": "test_student",
            "registration_number": "str123213ing",
            "sex": "F",
            "account": {
                "username": "student2",
                "password": "studentpassword2",
                "email": "student2@example.com",
            },
        }
        response_dict = self.call_update_student(**data, entity_id=student.id)
        id = self.assertKey(
            response_dict=response_dict, key="id", expected_type=int
        )
        student = Student.objects.filter(id=id).first()
        self.assertIsNotNone(student)
        self.assertIsNotNone(student.user)
        self.assertEqual(student.user.id, user.id)
        self.assertEqual(student.user.username, data["account"]["username"])
        self.assertEqual(student.user.email, data["account"]["email"])
        student.user.check_password(data["account"]["password"])

        data_old = data
        data = {
            "ci": "123214",
            "address": "address",
            "grade": 7,
            "last_name": "last_name",
            "first_name": "test_student",
            "registration_number": "str123213ing",
            "sex": "F",
            "account": {
                "username": "student3",
            },
        }
        response_dict = self.call_update_student(**data, entity_id=student.id)
        id = self.assertKey(
            response_dict=response_dict, key="id", expected_type=int
        )
        student = Student.objects.filter(id=id).first()
        self.assertIsNotNone(student)
        self.assertIsNotNone(student.user)
        self.assertEqual(student.user.id, user.id)
        self.assertEqual(student.user.username, data["account"]["username"])
        self.assertEqual(student.user.email, data_old["account"]["email"])
        student.user.check_password(data_old["account"]["password"])

        data = {
            "ci": "123214",
            "address": "address",
            "grade": 7,
            "last_name": "last_name",
            "first_name": "test_student",
            "registration_number": "str123213ing",
            "sex": "F",
            "account": {
                "password": "newpass",
            },
        }
        response_dict = self.call_update_student(**data, entity_id=student.id)
        id = self.assertKey(
            response_dict=response_dict, key="id", expected_type=int
        )
        student = Student.objects.filter(id=id).first()
        self.assertIsNotNone(student)
        self.assertIsNotNone(student.user)
        self.assertEqual(student.user.id, user.id)
        self.assertEqual(student.user.username, "student3")
        self.assertEqual(student.user.email, data_old["account"]["email"])
        student.user.check_password("newpass")

        data = {
            "ci": "123214",
            "address": "address2",
            "grade": 7,
            "last_name": "last_name2",
            "first_name": "test_student",
            "registration_number": "str123213ing",
            "sex": "F",
        }
        response_dict = self.call_update_student(**data, entity_id=student.id)
        id = self.assertKey(
            response_dict=response_dict, key="id", expected_type=int
        )
        student = Student.objects.filter(id=id).first()
        self.assertIsNotNone(student)
        self.assertIsNotNone(student.user)
        self.assertEqual(student.user.id, user.id)
        self.assertEqual(student.user.username, "student3")
        self.assertEqual(student.user.email, data_old["account"]["email"])
        student.user.check_password("newpass")

        User.objects.create(
            username="yaexiste", email="yaexiste@gmail.com", password="123"
        )
        data = {
            "ci": "123214",
            "address": "address",
            "grade": 7,
            "last_name": "last_name",
            "first_name": "test_student",
            "registration_number": "str123213ing",
            "sex": "F",
            "account": {
                "username": "yaexiste",
                "email": "yaexiste@gmail.com",
            },
        }
        self.call_update_student(
            **data,
            entity_id=student.id,
            bad_request=True,
            print_json_response=False,
        )
