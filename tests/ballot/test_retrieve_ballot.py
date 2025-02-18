from django.contrib.auth import get_user_model
from rest_framework.reverse import reverse

from apps.project.models import StudentCareer
from tests.ballot.parent_case.ballot_parent_case import BallotParentCase

User = get_user_model()


class TestRetrieveBallot(BallotParentCase):
    def call_get_ballot(
        self,
        entity_id: int,
        unauthorized: bool = False,
        forbidden: bool = False,
        bad_request: bool = False,
        not_found: bool = False,
        print_json_response: bool = False,
    ):
        URL = reverse("create-ballot", args=[entity_id])
        response_dict = self.call_retrieve(
            url=URL,
            unauthorized=unauthorized,
            forbidden=forbidden,
            bad_request=bad_request,
            not_found=not_found,
            print_json_response=print_json_response,
        )
        return response_dict

    def test_retrieve_ballot(self):
        student = self.students_9[0]
        response_dict = self.call_get_ballot(
            entity_id=student.id, print_json_response=True
        )
        self.assertEqual(
            response_dict,
            [
                student_career.career.name
                for student_career in StudentCareer.objects.filter(
                    student=student
                ).order_by("index")
            ],
        )
