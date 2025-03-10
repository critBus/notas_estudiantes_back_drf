from django.contrib.auth import get_user_model
from rest_framework.reverse import reverse

from apps.project.models import Student
from tests.student.parent_case.student_test_case import StudentTestCase

User = get_user_model()


class TestPostCanEditBallot(StudentTestCase):
    def call_can_edit_ballot(
        self,
        can_edit_bullet: bool = False,
        unauthorized: bool = False,
        forbidden: bool = False,
        bad_request: bool = False,
        not_found: bool = False,
        print_json_response: bool = False,
    ):
        URL = reverse("ballot-can-edit")
        response_dict = self.call_post(
            payload={"can_edit_bullet": can_edit_bullet},
            url=URL,
            unauthorized=unauthorized,
            forbidden=forbidden,
            bad_request=bad_request,
            not_found=not_found,
            print_json_response=print_json_response,
        )
        return response_dict

    def test_can_edit_ballot(self):
        self.create_random_student(can_edit_bullet=True)
        self.create_random_student()

        self.call_can_edit_ballot(
            can_edit_bullet=True, print_json_response=False
        )
        self.assertTrue(
            Student.objects.filter(can_edit_bullet=False).count() == 0
        )

        self.call_can_edit_ballot(can_edit_bullet=False)
        self.assertTrue(
            Student.objects.filter(can_edit_bullet=False).count() == 2
        )
