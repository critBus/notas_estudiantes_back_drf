from typing import Dict, Optional

from django.contrib.auth import get_user_model
from rest_framework.reverse import reverse  # Para generar urls

from apps.project.models import Professor
from tests.professor.parent_case.professor_parent_case import ProfessorTestCase

User = get_user_model()


class TestUpdateProfessor(ProfessorTestCase):
    def call_update_professor(
        self,
        entity_id: int,
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
        URL = reverse("professor-detail", args=[entity_id])

        payload = {
            "ci": ci,
            "address": address,
            "last_name": last_name,
            "first_name": first_name,
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

    def test_update_professor(self):
        professor = self.create_random_professor()
        data = {
            "ci": "123214",
            "address": "address",
            "last_name": "last_name",
            "first_name": "test_professor",
            "sex": "F",
        }
        response_dict = self.call_update_professor(
            **data, entity_id=professor.id, print_json_response=False
        )

        id = self.assertKey(
            response_dict=response_dict, key="id", expected_type=int
        )
        professor = Professor.objects.filter(id=id).first()
        self.assertIsNotNone(professor)
        self.assertIsNone(professor.user)

    def test_update_professor_account(self):
        professor = self.create_random_professor()
        data = {
            "ci": "123214",
            "address": "address",
            "last_name": "last_name",
            "first_name": "test_professor",
            "sex": "F",
            "account": {
                "username": "professor",
                "password": "professorpassword",
                "email": "professor@example.com",
            },
        }
        response_dict = self.call_update_professor(
            **data, entity_id=professor.id
        )
        id = self.assertKey(
            response_dict=response_dict, key="id", expected_type=int
        )
        professor = Professor.objects.filter(id=id).first()
        self.assertIsNotNone(professor)
        user = professor.user
        self.assertIsNotNone(user)
        self.assertEqual(professor.user.username, data["account"]["username"])
        self.assertEqual(professor.user.email, data["account"]["email"])
        professor.user.check_password(data["account"]["password"])

        data = {
            "ci": "123214",
            "address": "address",
            "last_name": "last_name",
            "first_name": "test_professor",
            "sex": "F",
            "account": {
                "username": "professor2",
                "password": "professorpassword2",
                "email": "professor2@example.com",
            },
        }
        response_dict = self.call_update_professor(
            **data, entity_id=professor.id
        )
        id = self.assertKey(
            response_dict=response_dict, key="id", expected_type=int
        )
        professor = Professor.objects.filter(id=id).first()
        self.assertIsNotNone(professor)
        self.assertIsNotNone(professor.user)
        self.assertEqual(professor.user.id, user.id)
        self.assertEqual(professor.user.username, data["account"]["username"])
        self.assertEqual(professor.user.email, data["account"]["email"])
        professor.user.check_password(data["account"]["password"])

        data_old = data
        data = {
            "ci": "123214",
            "address": "address",
            "last_name": "last_name",
            "first_name": "test_professor",
            "sex": "F",
            "account": {
                "username": "professor3",
            },
        }
        response_dict = self.call_update_professor(
            **data, entity_id=professor.id
        )
        id = self.assertKey(
            response_dict=response_dict, key="id", expected_type=int
        )
        professor = Professor.objects.filter(id=id).first()
        self.assertIsNotNone(professor)
        self.assertIsNotNone(professor.user)
        self.assertEqual(professor.user.id, user.id)
        self.assertEqual(professor.user.username, data["account"]["username"])
        self.assertEqual(professor.user.email, data_old["account"]["email"])
        professor.user.check_password(data_old["account"]["password"])

        data = {
            "ci": "123214",
            "address": "address",
            "last_name": "last_name",
            "first_name": "test_professor",
            "sex": "F",
            "account": {
                "password": "newpass",
            },
        }
        response_dict = self.call_update_professor(
            **data, entity_id=professor.id
        )
        id = self.assertKey(
            response_dict=response_dict, key="id", expected_type=int
        )
        professor = Professor.objects.filter(id=id).first()
        self.assertIsNotNone(professor)
        self.assertIsNotNone(professor.user)
        self.assertEqual(professor.user.id, user.id)
        self.assertEqual(professor.user.username, "professor3")
        self.assertEqual(professor.user.email, data_old["account"]["email"])
        professor.user.check_password("newpass")

        data = {
            "ci": "123214",
            "address": "address2",
            "last_name": "last_name2",
            "first_name": "test_professor",
            "sex": "F",
        }
        response_dict = self.call_update_professor(
            **data, entity_id=professor.id
        )
        id = self.assertKey(
            response_dict=response_dict, key="id", expected_type=int
        )
        professor = Professor.objects.filter(id=id).first()
        self.assertIsNotNone(professor)
        self.assertIsNotNone(professor.user)
        self.assertEqual(professor.user.id, user.id)
        self.assertEqual(professor.user.username, "professor3")
        self.assertEqual(professor.user.email, data_old["account"]["email"])
        professor.user.check_password("newpass")

        User.objects.create(
            username="yaexiste", email="yaexiste@gmail.com", password="123"
        )
        data = {
            "ci": "123214",
            "address": "address",
            "last_name": "last_name",
            "first_name": "test_professor",
            "sex": "F",
            "account": {
                "username": "yaexiste",
                "email": "yaexiste@gmail.com",
            },
        }
        self.call_update_professor(
            **data,
            entity_id=professor.id,
            bad_request=True,
            print_json_response=False,
        )
