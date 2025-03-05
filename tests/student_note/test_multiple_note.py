
from django.contrib.auth import get_user_model
from rest_framework.reverse import reverse  # Para generar urls

from apps.project.models import (
    SchoolYear,
    StudentNote,
    Subject,
)
from tests.student.parent_case.student_test_case import StudentTestCase

User = get_user_model()


class TestMultipleNotes(StudentTestCase):
    def call_multiple_note(
        self,
        pk: int,
        unauthorized: bool = False,
        forbidden: bool = False,
        bad_request: bool = False,
        not_found: bool = False,
        print_json_response: bool = False,
    ):
        URL = reverse("student-note-multiple", args=[pk])
        response_dict = self.call_get(
            url=URL,
            unauthorized=unauthorized,
            forbidden=forbidden,
            bad_request=bad_request,
            not_found=not_found,
            print_json_response=print_json_response,
        )

        return response_dict

    def test_multiple_notes(self):
        course = SchoolYear.get_current_course()
        subject = Subject.objects.first()
        student_1 = self.create_random_student(grade=subject.grade)
        student_2 = self.create_random_student(grade=subject.grade)
        student_3 = self.create_random_student(grade=subject.grade)

        note_1 = StudentNote.objects.create(
            subject=subject,
            student=student_1,
            school_year=course,
        )
        note_1.tcp1 = 90
        note_1.tcp2 = 79
        note_1.asc = 6
        note_1.final_exam = 92
        note_1.save()

        note_2 = StudentNote.objects.create(
            subject=subject,
            student=student_2,
            school_year=course,
        )
        note_2.tcp1 = 91
        note_2.tcp2 = 80
        note_2.asc = 7
        note_2.final_exam = 91
        note_2.save()

        response_dict = self.call_multiple_note(
            pk=subject.id, print_json_response=False
        )

        self.assertEqual(
            response_dict,
            [
                {
                    "id": note_1.id,
                    "asc": note_1.asc,
                    "final_exam": note_1.final_exam,
                    "tcp1": note_1.tcp1,
                    "tcp2": note_1.tcp2,
                    "student": note_1.student.id,
                    "subject": note_1.subject.id,
                },
                {
                    "id": note_2.id,
                    "asc": note_2.asc,
                    "final_exam": note_2.final_exam,
                    "tcp1": note_2.tcp1,
                    "tcp2": note_2.tcp2,
                    "student": note_2.student.id,
                    "subject": note_2.subject.id,
                },
                {
                    "student": student_3.id,
                    "subject": subject.id,
                    "asc": None,
                    "final_exam": None,
                    "tcp1": None,
                    "tcp2": None,
                },
            ],
        )
