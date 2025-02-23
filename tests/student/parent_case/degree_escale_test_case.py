from django.contrib.auth import get_user_model

from apps.project.models import (
    SchoolYear,
    StudentNote,
    Subject,
)
from tests.student.parent_case.student_test_case import StudentTestCase

User = get_user_model()


class DegreeEscaleTestCase(StudentTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.maxDiff = None

    def create_fake_ranking(self):
        SchoolYear.objects.all().delete()
        Subject.objects.all().delete()
        curse_7, curse_8, curse_9 = self.create_3_school_year(2022)
        for i in range(3):
            grade = i + 7
            Subject.objects.create(
                grade=grade, name=f"test_{grade}", tcp2_required=True
            )
        students = []
        for i in range(3):
            student = self.create_random_student(grade=9)
            students.append(student)
            for j in range(3):
                grade = j + 7
                note = StudentNote.objects.create(
                    subject=Subject.objects.get(name=f"test_{grade}"),
                    student=student,
                    school_year=SchoolYear.objects.get(
                        start_date__year=2022 + j
                    ),
                )
                note.tcp1 = 90 + i + j
                note.tcp2 = 79 + i + j
                note.asc = 6 + i + j
                note.final_exam = 92 + i + j
                note.save()
        students.reverse()
        return students
