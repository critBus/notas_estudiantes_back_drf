from django.contrib.auth import get_user_model

from apps.project.models import SchoolYear, StudentNote
from tests.student.parent_case.student_test_case import StudentTestCase

User = get_user_model()


class TestValidNote(StudentTestCase):
    def test_is_valid_note(self):
        course = SchoolYear.get_current_course()
        subject = self.subjects[0]
        student = self.create_random_student(grade=9)
        nota = StudentNote.objects.create(
            subject=subject, student=student, school_year=course
        )
        nota.tcp1 = 60
        nota.tcp2 = 60
        nota.asc = 6
        nota.final_exam = 60

        self.assertTrue(StudentNote.are_valid([nota]))

        nota.tcp1 = 100
        nota.tcp2 = 100
        nota.asc = 10
        nota.final_exam = 100

        self.assertTrue(StudentNote.are_valid([nota]))

        subject.tcp2_required = True
        subject.save()
        nota.save()
        nota.refresh_from_db()
        self.assertTrue(StudentNote.are_valid([nota]))

    def test_their_notes_are_valid(self):
        student = self.create_random_student(grade=9)
        self.ponerle_notas_validas_al_estudiante(student=student)
        self.assertTrue(student.their_notes_are_valid())
