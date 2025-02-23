from django.contrib.auth import get_user_model
from rest_framework.reverse import reverse

from apps.project.models import Student, StudentCareer
from tests.ballot.parent_case.ballot_parent_case import BallotParentCase

User = get_user_model()


class TestListBallot(BallotParentCase):
    def call_list_ballot(
        self,
        unauthorized: bool = False,
        forbidden: bool = False,
        bad_request: bool = False,
        not_found: bool = False,
        print_json_response: bool = False,
    ):
        response_dict = self.call_get(
            url=reverse("ballot-list"),
            unauthorized=unauthorized,
            forbidden=forbidden,
            bad_request=bad_request,
            not_found=not_found,
            print_json_response=print_json_response,
        )

        return response_dict

    def test_list_ballots(self):
        response_dict = self.call_list_ballot(print_json_response=False)
        self.assertDictEqual(
            response_dict,
            {
                "count": 20,
                "next": "http://testserver/api/students/ballot/?page=2",
                "previous": None,
                "results": [
                    {
                        "id": student.id,
                        "is_approved": False,
                        "ballot": [
                            student_career.career.name
                            for student_career in StudentCareer.objects.filter(
                                student=student
                            ).order_by("index")
                        ],
                        "ci": student.ci,
                        "address": student.address,
                        "grade": 9,
                        "last_name": student.last_name,
                        "first_name": student.first_name,
                        "registration_number": student.registration_number,
                        "sex": student.sex,
                        "is_graduated": False,
                        "is_dropped_out": False,
                        "user": None,
                    }
                    for student in Student.objects.order_by("ci")[:10]
                ],
            },
        )

        StudentCareer.objects.all().delete()
        response_dict = self.call_list_ballot(print_json_response=False)
        self.assertDictEqual(
            response_dict,
            {
                "count": 0,
                "next": None,
                "previous": None,
                "results": [],
            },
        )
