from django.contrib.auth import get_user_model

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
        for student in students[:-1]:
            self.add_ballot_to_student(student=student)
        self.assertTrue(Student.are_missing_ballots())
        self.add_ballot_to_student(student=students[-1])
        self.assertFalse(Student.are_missing_ballots())
