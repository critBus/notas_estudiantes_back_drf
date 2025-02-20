from django.contrib.auth import get_user_model
from django.utils import timezone

from apps.project.models import Dropout
from tests.student.parent_case.student_test_case import StudentTestCase

User = get_user_model()


class TestVaja(StudentTestCase):
    def test_vaja(self):
        student = self.create_random_student(grade=7)
        self.assertEqual(False, student.is_dropped_out)
        dropout = Dropout.objects.create(
            student=student,
            date=timezone.now().date(),
            municipality="municipality",
            province="province",
            school="school",
        )
        self.assertTrue(student.is_dropped_out)
        dropout.delete()
        self.assertEqual(False, student.is_dropped_out)

        student_2 = self.create_random_student(grade=7)
        dropout_2 = Dropout.objects.create(
            student=student_2,
            date=timezone.now().date(),
            municipality="municipality",
            province="province",
            school="school",
        )
        self.assertTrue(student_2.is_dropped_out)

        dropout_2.student = student
        dropout_2.save()
        self.assertTrue(student.is_dropped_out)
        student_2.refresh_from_db()
        self.assertEqual(False, student_2.is_dropped_out)
