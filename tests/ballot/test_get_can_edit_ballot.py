from django.contrib.auth import get_user_model
from rest_framework.reverse import reverse

from tests.student.parent_case.student_test_case import StudentTestCase

User = get_user_model()


class TestCanEditBallot(StudentTestCase):
    def call_can_edit_ballot(
        self,
        unauthorized: bool = False,
        forbidden: bool = False,
        bad_request: bool = False,
        not_found: bool = False,
        print_json_response: bool = False,
    ):
        URL = reverse("ballot-can-edit")
        response_dict = self.call_get(
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
        student_2 = self.create_random_student()

        response_dict = self.call_can_edit_ballot()
        self.assertDictEqual(response_dict, {"can_edit_bullet": False})

        student_2.can_edit_bullet = True
        student_2.save()

        response_dict = self.call_can_edit_ballot()
        self.assertDictEqual(response_dict, {"can_edit_bullet": True})
