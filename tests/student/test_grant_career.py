from django.contrib.auth import get_user_model
from rest_framework.reverse import reverse

from apps.project.models import (
    ApprovedSchoolCourse,
    Career,
    DegreeScale,
    GrantCareer,
    SchoolYear,
    Student,
    StudentCareer,
)
from tests.student.parent_case.degree_escale_test_case import (
    DegreeEscaleTestCase,
)

User = get_user_model()


class TestGrantCareer(DegreeEscaleTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.careers_names = [f"career{i}" for i in range(20)]
        self.careers = []
        for i, name in enumerate(self.careers_names):
            self.careers.append(Career.objects.create(name=name, amount=1))

    def add_ballot_to_student(
        self,
        student: Student,
        initial_index: int = 0,
        amount_to_agregate: int = 10,
    ):
        for i in range(amount_to_agregate):
            index = (10 - amount_to_agregate) + i + 1
            StudentCareer.objects.create(
                student=student,
                career=self.careers[initial_index + i],
                index=index,
            )

    def create_ballots_to_students(self):
        students = self.create_fake_ranking()

        StudentCareer.objects.create(
            student=students[0], career=self.careers[0], index=1
        )
        self.add_ballot_to_student(students[0], 1, amount_to_agregate=9)

        StudentCareer.objects.create(
            student=students[1], career=self.careers[2], index=1
        )
        self.add_ballot_to_student(students[1], 1, amount_to_agregate=9)

        StudentCareer.objects.create(
            student=students[2], career=self.careers[0], index=1
        )
        StudentCareer.objects.create(
            student=students[2], career=self.careers[1], index=1
        )
        self.add_ballot_to_student(students[2], 1, amount_to_agregate=8)
        return (students, [self.careers[0], self.careers[2], self.careers[1]])

    def test_grant_career(self):
        students, careers = self.create_ballots_to_students()
        DegreeScale.calculate_all_ranking_number()
        course = SchoolYear.get_current_course()
        GrantCareer.grant()
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
                    },
                    "approved_school_course": {
                        "id": grant.approved_school_course.id,
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
                        },
                        "school_year": {
                            "id": grant.approved_school_course.school_year.id,
                            "start_date": str(
                                grant.approved_school_course.school_year.start_date
                            ),
                            "end_date": str(
                                grant.approved_school_course.school_year.end_date
                            ),
                            "name": grant.approved_school_course.school_year.name,
                        },
                        "date": str(grant.approved_school_course.date),
                        "grade": 9,
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
                    },
                    "approved_school_course": {
                        "id": grant.approved_school_course.id,
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
                        },
                        "school_year": {
                            "id": grant.approved_school_course.school_year.id,
                            "start_date": str(
                                grant.approved_school_course.school_year.start_date
                            ),
                            "end_date": str(
                                grant.approved_school_course.school_year.end_date
                            ),
                            "name": grant.approved_school_course.school_year.name,
                        },
                        "date": str(grant.approved_school_course.date),
                        "grade": 9,
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
