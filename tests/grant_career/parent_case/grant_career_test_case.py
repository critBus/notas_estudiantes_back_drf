from django.contrib.auth import get_user_model

from apps.project.models import (
    Career,
    Student,
    StudentCareer,
)
from tests.student.parent_case.degree_escale_test_case import (
    DegreeEscaleTestCase,
)

User = get_user_model()


class GrantCareerTestCase(DegreeEscaleTestCase):
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
