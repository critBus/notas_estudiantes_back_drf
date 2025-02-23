from typing import List

from django.contrib.auth import get_user_model
from rest_framework.reverse import reverse  # Para generar urls

from apps.project.models import Career, StudentCareer
from tests.student.parent_case.student_test_case import StudentTestCase

User = get_user_model()


class TestCreateBallot(StudentTestCase):
    def call_create_ballot(
        self,
        student_id: int,
        careers_names: List[str],
        unauthorized: bool = False,
        forbidden: bool = False,
        bad_request: bool = False,
        print_json_response: bool = False,
        not_found=False,
    ):
        URL = reverse("create-ballot", args=[student_id])

        payload = {"list_career_name": careers_names}

        return self.call_create(
            url=URL,
            payload=payload,
            unauthorized=unauthorized,
            forbidden=forbidden,
            bad_request=bad_request,
            not_found=not_found,
            print_json_response=print_json_response,
            format_json=True,
        )

    def test_create_ballot(self):
        student = self.create_random_student(grade=9)
        careers_names = [f"career{i}" for i in range(10)]
        for name in careers_names:
            Career.objects.create(name=name, amount=1)

        student_7 = self.create_random_student(grade=7)
        self.call_create_ballot(
            student_id=student_7.id,
            careers_names=careers_names,
            bad_request=False,
            print_json_response=False,
            not_found=True,
        )

        careers_names_incorrect = careers_names.copy()
        careers_names_incorrect.pop(1)

        self.call_create_ballot(
            student_id=student.id,
            careers_names=careers_names_incorrect,
            bad_request=True,
            print_json_response=False,
            not_found=False,
        )

        careers_names_incorrect.append("careers11")
        self.call_create_ballot(
            student_id=student.id,
            careers_names=careers_names_incorrect,
            bad_request=True,
            print_json_response=False,
            not_found=False,
        )

        self.call_create_ballot(
            student_id=student.id,
            careers_names=careers_names,
            bad_request=False,
            print_json_response=False,
            not_found=False,
        )

        q = StudentCareer.objects.filter(student=student)
        self.assertEqual(q.count(), 10)
        for i, student_career in enumerate(q.order_by("index")):
            self.assertEqual(student_career.career.name, careers_names[i])

        careers_names[1] = careers_names[0]
        self.call_create_ballot(
            student_id=student.id,
            careers_names=careers_names,
            bad_request=True,
            print_json_response=True,
            not_found=False,
        )
