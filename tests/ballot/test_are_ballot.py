from django.contrib.auth import get_user_model
from rest_framework.reverse import reverse

from apps.project.models import Career, Student, StudentCareer
from tests.student.parent_case.student_test_case import StudentTestCase

User = get_user_model()


class TestAreBallot(StudentTestCase):
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

    def test_are_ballot(self):
        self.assertTrue(Student.are_missing_ballots())
        students = [self.create_random_student(grade=9) for _ in range(10)]
        self.assertTrue(Student.are_missing_ballots())

        for student in students[1:]:
            self.ponerle_notas_validas_al_estudiante(student=student)
        self.assertTrue(Student.are_missing_ballots())
        self.ponerle_notas_validas_al_estudiante(student=students[0])
        self.assertTrue(Student.are_missing_ballots())

        for student in students[:-1]:
            self.add_ballot_to_student(student=student)
        self.assertTrue(Student.are_missing_ballots())
        self.add_ballot_to_student(student=students[-1])

        self.assertFalse(Student.are_missing_ballots())

    def call_are_ballot(
        self,
        are_ballot: bool,
        unauthorized: bool = False,
        forbidden: bool = False,
        bad_request: bool = False,
        not_found: bool = False,
        print_json_response: bool = False,
    ):
        URL = reverse("ballot-are-missing")
        response_dict = self.call_get(
            url=URL,
            unauthorized=unauthorized,
            forbidden=forbidden,
            bad_request=bad_request,
            not_found=not_found,
            print_json_response=print_json_response,
        )
        if response_dict:
            self.validate_are_ballot(
                response_dict=response_dict, are_ballot=are_ballot
            )
        return response_dict

    def validate_are_ballot(self, response_dict, are_ballot=False):
        self.assertEqual(are_ballot, not Student.are_missing_ballots())
        self.assertDictEqual(
            response_dict, {"are_missing_ballots": not are_ballot}
        )

    def test_are_missing_ballots(self):
        self.call_are_ballot(are_ballot=False)
        students = [self.create_random_student(grade=9) for _ in range(10)]
        self.assertTrue(Student.are_missing_ballots())
        for student in students[:-1]:
            self.add_ballot_to_student(student=student)
        self.call_are_ballot(are_ballot=False)
        self.add_ballot_to_student(student=students[-1])
        self.call_are_ballot(are_ballot=False)

        for student in students[1:]:
            self.ponerle_notas_validas_al_estudiante(student=student)

        self.call_are_ballot(are_ballot=True)
