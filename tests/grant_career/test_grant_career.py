from django.contrib.auth import get_user_model
from rest_framework.reverse import reverse

from apps.project.models import (
    ApprovedSchoolCourse,
    DegreeScale,
    GrantCareer,
    SchoolYear,
    Student,
)
from tests.grant_career.parent_case.grant_career_test_case import (
    GrantCareerTestCase,
)

User = get_user_model()


class TestGrantCareer(GrantCareerTestCase):
    def test_grant_career(self):
        students, careers = self.create_ballots_to_students()
        DegreeScale.calculate_all_ranking_number()
        course = SchoolYear.get_current_course()
        GrantCareer.grant()
        q = GrantCareer.objects.all()
        Student.graduate_all()
        qa = ApprovedSchoolCourse.objects.all()
        self.assertEqual(q.count(), 3)
        self.assertEqual(qa.count(), 3)
        for i, student in enumerate(students):
            self.assertTrue(
                q.filter(student=student, career=careers[i]).exists()
            )
            self.assertTrue(
                qa.filter(student=student, school_year=course, grade=9).exists()
            )

    def call_grant_career(
        self,
        unauthorized: bool = False,
        forbidden: bool = False,
        bad_request: bool = False,
        not_found: bool = False,
        print_json_response: bool = False,
    ):
        URL = reverse("grant-career-grant")
        response_dict = self.call_get(
            url=URL,
            unauthorized=unauthorized,
            forbidden=forbidden,
            bad_request=bad_request,
            not_found=not_found,
            print_json_response=print_json_response,
        )

        return response_dict

    def test_grant_career_view(self):
        students, careers = self.create_ballots_to_students()
        DegreeScale.calculate_all_ranking_number()

        response_dict = self.call_grant_career(print_json_response=False)
        Student.graduate_all()
        course = SchoolYear.get_current_course()
        q = GrantCareer.objects.all()
        qa = ApprovedSchoolCourse.objects.all()
        self.assertEqual(q.count(), 3)
        self.assertEqual(qa.count(), 3)
        for i, student in enumerate(students):
            self.assertTrue(
                q.filter(student=student, career=careers[i]).exists()
            )
            self.assertTrue(
                qa.filter(student=student, school_year=course, grade=9).exists()
            )

        self.assertEqual(
            response_dict,
            [
                {
                    "id": grant.id,
                    "student": {
                        "id": grant.student.id,
                        "is_approved": True,
                        "ci": grant.student.ci,
                        "address": grant.student.address,
                        "grade": grant.student.grade,
                        "last_name": grant.student.last_name,
                        "first_name": grant.student.first_name,
                        "registration_number": grant.student.registration_number,
                        "sex": grant.student.sex,
                        "is_graduated": False,
                        "is_dropped_out": False,
                        "user": None,
                        "group": None,
                        "can_edit_bullet": False,
                    },
                    "school_year": {
                        "id": grant.school_year.id,
                        "start_date": str(grant.school_year.start_date),
                        "end_date": str(grant.school_year.end_date),
                        "name": grant.school_year.name,
                    },
                    "career": {
                        "id": grant.career.id,
                        "amount": grant.career.amount,
                        "name": grant.career.name,
                    },
                }
                for grant in [
                    GrantCareer.objects.get(student=v) for v in students
                ]
            ],
        )

    def call_grant_career_current(
        self,
        unauthorized: bool = False,
        forbidden: bool = False,
        bad_request: bool = False,
        not_found: bool = False,
        print_json_response: bool = False,
    ):
        URL = reverse("grant-career-current")
        response_dict = self.call_get(
            url=URL,
            unauthorized=unauthorized,
            forbidden=forbidden,
            bad_request=bad_request,
            not_found=not_found,
            print_json_response=print_json_response,
        )

        return response_dict

    def test_grant_career_current_view(self):
        students, careers = self.create_ballots_to_students()
        DegreeScale.calculate_all_ranking_number()
        GrantCareer.grant()
        Student.graduate_all()

        response_dict = self.call_grant_career_current(
            print_json_response=False
        )
        course = SchoolYear.get_current_course()

        q = GrantCareer.objects.all()
        qa = ApprovedSchoolCourse.objects.all()
        self.assertEqual(q.count(), 3)
        self.assertEqual(qa.count(), 3)
        for i, student in enumerate(students):
            self.assertTrue(
                q.filter(student=student, career=careers[i]).exists()
            )
            self.assertTrue(
                qa.filter(student=student, school_year=course, grade=9).exists()
            )

        self.assertEqual(
            response_dict,
            [
                {
                    "id": grant.id,
                    "student": {
                        "id": grant.student.id,
                        "is_approved": True,
                        "ci": grant.student.ci,
                        "address": grant.student.address,
                        "grade": grant.student.grade,
                        "last_name": grant.student.last_name,
                        "first_name": grant.student.first_name,
                        "registration_number": grant.student.registration_number,
                        "sex": grant.student.sex,
                        "is_graduated": True,
                        "is_dropped_out": False,
                        "user": None,
                        "group": None,
                        "can_edit_bullet": False,
                    },
                    "school_year": {
                        "id": grant.school_year.id,
                        "start_date": str(grant.school_year.start_date),
                        "end_date": str(grant.school_year.end_date),
                        "name": grant.school_year.name,
                    },
                    "career": {
                        "id": grant.career.id,
                        "amount": grant.career.amount,
                        "name": grant.career.name,
                    },
                }
                for grant in [
                    GrantCareer.objects.get(student=v) for v in students
                ]
            ],
        )
