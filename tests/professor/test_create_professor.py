from typing import Dict, Optional

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework.reverse import reverse  # Para generar urls

from apps.project.models import ROL_NAME_STUDENT, Professor
from tests.professor.parent_case.professor_parent_case import ProfessorTestCase

User = get_user_model()


class TestCreateProfessor(ProfessorTestCase):
    def call_create_professor(
        self,
        ci: str,
        address: str,
        last_name: str,
        first_name: str,
        sex: str,
        account: Optional[Dict[str, str]] = None,
        unauthorized: bool = False,
        forbidden: bool = False,
        bad_request: bool = False,
        print_json_response: bool = False,
    ):
        URL = reverse("professor-list")

        payload = {
            "ci": ci,
            "address": address,
            "last_name": last_name,
            "first_name": first_name,
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

    def test_add_professor(self):
        data = {
            "ci": "123214",
            "address": "address",
            "last_name": "last_name",
            "first_name": "test_professor",
            "sex": "F",
        }
        response_dict = self.call_create_professor(**data)
        id = self.assertKey(
            response_dict=response_dict, key="id", expected_type=int
        )
        professor = Professor.objects.filter(id=id).first()
        self.assertIsNotNone(professor)
        self.assertIsNone(professor.user)

    def test_add_professor_account(self):
        data = {
            "ci": "123214",
            "address": "address",
            "last_name": "last_name",
            "first_name": "test_professor",
            "sex": "M",
            "account": {
                "username": "professor",
                "password": "professorpassword",
                "email": "professor@example.com",
            },
        }
        response_dict = self.call_create_professor(**data)
        id = self.assertKey(
            response_dict=response_dict, key="id", expected_type=int
        )
        professor = Professor.objects.filter(id=id).first()
        self.assertIsNotNone(professor)
        self.assertIsNotNone(professor.user)

        self.assertEqual(professor.user.username, data["account"]["username"])
        self.assertEqual(professor.user.email, data["account"]["email"])
        professor.user.check_password(data["account"]["password"])
        self.assertTrue(
            Group.objects.filter(
                user=professor.user, name=ROL_NAME_STUDENT
            ).exists()
        )

        data = {
            "ci": "12321232114",
            "address": "address2",
            "last_name": "last_name2",
            "first_name": "test_professor2",
            "sex": "F",
            "account": {
                "username": "professor",
                "password": "professorpassword",
                "email": "professor@example.com",
            },
        }
        self.call_create_professor(
            **data, bad_request=True, print_json_response=False
        )
