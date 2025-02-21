from typing import List

from django.contrib.auth import get_user_model
from rest_framework.reverse import reverse

from apps.project.models import (
    ApprovedSchoolCourse,
    Career,
    DegreeScale,
    Student,
    StudentCareer,
)
from tests.student.parent_case.degree_escale_test_case import (
    DegreeEscaleTestCase,
)

User = get_user_model()


class TestUpgradingAll(DegreeEscaleTestCase):
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

    def call_upgrading_all(
        self,
        unauthorized: bool = False,
        forbidden: bool = False,
        bad_request: bool = False,
        not_found: bool = False,
        print_json_response: bool = False,
    ):
        URL = reverse("upgrading-all")
        response_dict = self.call_get(
            url=URL,
            unauthorized=unauthorized,
            forbidden=forbidden,
            bad_request=bad_request,
            not_found=not_found,
            print_json_response=print_json_response,
        )

        return response_dict

    def test_upgrading_all(self):
        self.call_upgrading_all(bad_request=True, print_json_response=False)
        students, careers = self.create_ballots_to_students()
        self.call_upgrading_all(bad_request=True, print_json_response=False)
        DegreeScale.calculate_all_ranking_number()
        self.call_upgrading_all(bad_request=False, print_json_response=False)

        self.call_upgrading_all(bad_request=True, print_json_response=True)

    def validate_course(self, students: List[Student], grade: int):
        for student in students:
            student.refresh_from_db()
            self.assertEqual(student.grade, grade if grade == 9 else grade + 1)
            self.assertTrue(
                ApprovedSchoolCourse.objects.filter(
                    student=student, grade=grade
                ).exists()
            )

    def test_upgrading_all_7_8_9(self):
        students_9, careers = self.create_ballots_to_students()
        DegreeScale.calculate_all_ranking_number()

        students_7 = [self.create_random_student(grade=7) for _ in range(3)]
        for student in students_7:
            self.ponerle_notas_validas_al_estudiante(student=student)

        students_8 = [self.create_random_student(grade=8) for _ in range(3)]
        for student in students_8:
            self.ponerle_notas_validas_al_estudiante(student=student)

        self.call_upgrading_all(bad_request=False, print_json_response=False)
        self.validate_course(students_9, 9)
        self.validate_course(students_8, 8)
        self.validate_course(students_7, 7)
