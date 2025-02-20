from django.contrib.auth import get_user_model

from apps.project.models import Career, StudentCareer
from tests.student.parent_case.student_test_case import StudentTestCase

User = get_user_model()


class BallotParentCase(StudentTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.students_9 = []
        self.careers_names = [f"career{i}" for i in range(20)]
        self.careers = []
        for i, name in enumerate(self.careers_names):
            self.careers.append(Career.objects.create(name=name, amount=i))
        for i in range(20):
            student = self.create_random_student(grade=9)
            for j in range(10):
                StudentCareer.objects.create(
                    student=student, career=self.careers[(i + j) % 20], index=j
                )
            self.students_9.append(student)
        self.students_9 = sorted(self.students_9, key=lambda v: v.ci)
        self.maxDiff = None
