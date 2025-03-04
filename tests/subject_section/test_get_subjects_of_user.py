from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework.reverse import reverse  # Para generar urls

from apps.project.models import (
    ROL_NAME_PROFESSOR,
    ROL_NAME_STUDENT,
    Subject,
)
from tests.professor.mixin.professor_mixin import ProfessorMixin
from tests.student.parent_case.student_test_case import StudentTestCase

User = get_user_model()


class TestSubjectOfUser(StudentTestCase, ProfessorMixin):
    def call_get_subject_of_user(
        self,
        unauthorized: bool = False,
        forbidden: bool = False,
        bad_request: bool = False,
        not_found: bool = False,
        print_json_response: bool = False,
    ):
        URL = reverse("subject-section-subjects")
        response_dict = self.call_get(
            url=URL,
            unauthorized=unauthorized,
            forbidden=forbidden,
            bad_request=bad_request,
            not_found=not_found,
            print_json_response=print_json_response,
        )

        return response_dict

    def test_subject_of_user(self):
        student_user = User.objects.create_user(
            username="student", password="student", email="student@gmail.com"
        )
        group_student = Group.objects.get(name=ROL_NAME_STUDENT)
        student_user.groups.add(group_student)
        self.create_random_student(user=student_user, grade=8)

        self.login(username=student_user.username, password="student")
        self.put_authentication_in_the_header()

        response_dict = self.call_get_subject_of_user(print_json_response=False)
        subjects_math = Subject.objects.get(name="Math_8")
        subjects_cience = Subject.objects.get(name="Cience_8")
        subjects_english = Subject.objects.get(name="English_8")
        self.assertEqual(
            response_dict,
            [
                {
                    "id": subjects_cience.id,
                    "professor": [],
                    "grade": 8,
                    "name": "Cience_8",
                    "tcp2_required": False,
                },
                {
                    "id": subjects_english.id,
                    "professor": [],
                    "grade": 8,
                    "name": "English_8",
                    "tcp2_required": False,
                },
                {
                    "id": subjects_math.id,
                    "professor": [],
                    "grade": 8,
                    "name": "Math_8",
                    "tcp2_required": False,
                },
            ],
        )

        professor_user = User.objects.create_user(
            username="professor",
            password="professor",
            email="professor@gmail.com",
        )
        group_professor = Group.objects.get(name=ROL_NAME_PROFESSOR)
        professor_user.groups.add(group_professor)
        professor = self.create_random_professor(user=professor_user)
        subjects_cience.professor.add(professor)
        subjects_math.professor.add(professor)
        self.login(username=professor_user.username, password="professor")
        self.put_authentication_in_the_header()

        response_dict = self.call_get_subject_of_user(print_json_response=False)
        self.assertEqual(
            response_dict,
            [
                {
                    "id": subjects_cience.id,
                    "professor": [
                        {
                            "id": professor.id,
                            "ci": professor.ci,
                            "address": professor.address,
                            "last_name": professor.last_name,
                            "first_name": professor.first_name,
                            "sex": professor.sex,
                            "user": professor_user.id,
                        }
                    ],
                    "grade": 8,
                    "name": "Cience_8",
                    "tcp2_required": False,
                },
                {
                    "id": subjects_math.id,
                    "professor": [
                        {
                            "id": professor.id,
                            "ci": professor.ci,
                            "address": professor.address,
                            "last_name": professor.last_name,
                            "first_name": professor.first_name,
                            "sex": professor.sex,
                            "user": professor_user.id,
                        }
                    ],
                    "grade": 8,
                    "name": "Math_8",
                    "tcp2_required": False,
                },
            ],
        )

        Subject.objects.filter(grade__in=[7, 9]).delete()
        self.login_superuser()
        response_dict = self.call_get_subject_of_user(print_json_response=False)
        self.assertEqual(
            response_dict,
            [
                {
                    "id": subjects_cience.id,
                    "professor": [
                        {
                            "id": professor.id,
                            "ci": professor.ci,
                            "address": professor.address,
                            "last_name": professor.last_name,
                            "first_name": professor.first_name,
                            "sex": professor.sex,
                            "user": professor_user.id,
                        }
                    ],
                    "grade": 8,
                    "name": "Cience_8",
                    "tcp2_required": False,
                },
                {
                    "id": subjects_english.id,
                    "professor": [],
                    "grade": 8,
                    "name": "English_8",
                    "tcp2_required": False,
                },
                {
                    "id": subjects_math.id,
                    "professor": [
                        {
                            "id": professor.id,
                            "ci": professor.ci,
                            "address": professor.address,
                            "last_name": professor.last_name,
                            "first_name": professor.first_name,
                            "sex": professor.sex,
                            "user": professor_user.id,
                        }
                    ],
                    "grade": 8,
                    "name": "Math_8",
                    "tcp2_required": False,
                },
            ],
        )
