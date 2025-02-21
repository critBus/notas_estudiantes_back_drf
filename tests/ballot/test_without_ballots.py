from django.contrib.auth import get_user_model

from apps.project.models import Career, Student, StudentCareer
from tests.student.parent_case.student_test_case import StudentTestCase

User = get_user_model()


class TestWihoutBallots(StudentTestCase):
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

    def validate_are_missing_ballots(self, are_missing_ballots, force=None):
        self.assertEqual(are_missing_ballots, Student.are_missing_ballots())
        self.assertEqual(
            are_missing_ballots if force is None else force,
            len(Student.get_students_without_ballots()) > 0,
        )

    def test_are_ballot(self):
        self.validate_are_missing_ballots(True, force=False)
        students = [self.create_random_student(grade=9) for _ in range(10)]
        self.validate_are_missing_ballots(True)

        for student in students[1:]:
            self.ponerle_notas_validas_al_estudiante(student=student)
        self.validate_are_missing_ballots(True)
        self.ponerle_notas_validas_al_estudiante(student=students[0])
        self.validate_are_missing_ballots(True)

        for student in students[:-1]:
            self.add_ballot_to_student(student=student)
        self.validate_are_missing_ballots(True)
        self.add_ballot_to_student(student=students[-1])
        self.validate_are_missing_ballots(False)
