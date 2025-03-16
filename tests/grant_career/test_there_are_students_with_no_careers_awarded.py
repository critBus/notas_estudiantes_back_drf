from django.contrib.auth import get_user_model

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
    def validate_are_students_with_no_careers(
        self, are_students_with_no_careers: bool
    ):
        self.assertEqual(
            are_students_with_no_careers,
            GrantCareer.there_are_students_with_no_careers_awarded(),
        )

    def test_there_are_students_with_no_careers_awarded(self):
        self.validate_are_students_with_no_careers(True)

        students, careers = self.create_ballots_to_students()
        DegreeScale.calculate_all_ranking_number()
        course = SchoolYear.get_current_course()
        self.validate_are_students_with_no_careers(True)

        GrantCareer.grant()
        self.validate_are_students_with_no_careers(False)

        GrantCareer.objects.first().delete()
        self.validate_are_students_with_no_careers(True)

        GrantCareer.grant()
        self.validate_are_students_with_no_careers(False)
