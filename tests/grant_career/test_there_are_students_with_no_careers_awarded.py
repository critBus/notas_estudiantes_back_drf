from django.contrib.auth import get_user_model
from rest_framework.reverse import reverse

from apps.project.models import (
    DegreeScale,
    GrantCareer,
    SchoolYear,
)
from tests.grant_career.parent_case.grant_career_test_case import (
    GrantCareerTestCase,
)

User = get_user_model()


class TestThereAreStudentsWithNoCareersAwarded(GrantCareerTestCase):
    def call_grant_career_without_granting(
        self,
        unauthorized: bool = False,
        forbidden: bool = False,
        bad_request: bool = False,
        not_found: bool = False,
        print_json_response: bool = False,
    ):
        URL = reverse("grant-career-without-granting")
        response_dict = self.call_get(
            url=URL,
            unauthorized=unauthorized,
            forbidden=forbidden,
            bad_request=bad_request,
            not_found=not_found,
            print_json_response=print_json_response,
        )
        return response_dict

    def validate_are_students_with_no_careers(
        self, are_students_with_no_careers: bool
    ):
        self.assertEqual(
            are_students_with_no_careers,
            GrantCareer.there_are_students_with_no_careers_awarded(),
        )
        response_dict = self.call_grant_career_without_granting()
        self.assertDictEqual(
            response_dict, {"without_granting": are_students_with_no_careers}
        )

    def test_there_are_students_with_no_careers_awarded(self):
        self.validate_are_students_with_no_careers(True)

        students, careers = self.create_ballots_to_students()
        DegreeScale.calculate_all_ranking_number()
        SchoolYear.get_current_course()
        self.validate_are_students_with_no_careers(True)

        GrantCareer.grant()
        self.validate_are_students_with_no_careers(False)

        GrantCareer.objects.first().delete()
        self.validate_are_students_with_no_careers(True)

        GrantCareer.grant()
        self.validate_are_students_with_no_careers(False)
