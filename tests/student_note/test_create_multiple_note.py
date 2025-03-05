from typing import Any, Dict, List

from django.contrib.auth import get_user_model
from rest_framework.reverse import reverse  # Para generar urls

from apps.project.models import (
    SchoolYear,
    StudentNote,
    Subject,
)
from tests.student.parent_case.student_test_case import StudentTestCase

User = get_user_model()


class TestCreateMultipleNotes(StudentTestCase):
    def call_create_multiple_note(
        self,
        payload: List[Dict[str, Any]],
        unauthorized: bool = False,
        forbidden: bool = False,
        bad_request: bool = False,
        not_found: bool = False,
        print_json_response: bool = False,
    ):
        URL = reverse("student-note-create-multiple")
        response_dict = self.call_post(
            payload=payload,
            url=URL,
            unauthorized=unauthorized,
            forbidden=forbidden,
            bad_request=bad_request,
            not_found=not_found,
            print_json_response=print_json_response,
            format_json=True,
        )

        return response_dict

    def test_multiple_notes(self):
        StudentNote.objects.all().delete()
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

        payload = [
            {
                "id": note_1.id,
                "asc": note_1.asc + 1,
                "final_exam": note_1.final_exam + 1,
                "tcp1": note_1.tcp1 + 1,
                "tcp2": note_1.tcp2,
                "student": note_1.student.id,
                "subject": note_1.subject.id,
            },
            {
                "id": note_2.id,
                "asc": note_2.asc,
                "final_exam": note_2.final_exam,
                "tcp1": note_2.tcp1 + 1,
                "tcp2": note_2.tcp2 + 1,
                "student": note_2.student.id,
                "subject": note_2.subject.id,
            },
            {
                "asc": 6,
                "final_exam": 61,
                "tcp1": 68,
                "tcp2": 56,
                "student": student_3.id,
                "subject": subject.id,
            },
        ]
        self.call_create_multiple_note(
            payload=payload, print_json_response=False
        )

        self.assertEqual(3, StudentNote.objects.count())
        note_1.refresh_from_db()
        note_2.refresh_from_db()
        self.assertEqual(note_1.asc, payload[0]["asc"])
        self.assertEqual(note_1.final_exam, payload[0]["final_exam"])
        self.assertEqual(note_1.tcp1, payload[0]["tcp1"])
        self.assertEqual(note_1.tcp2, payload[0]["tcp2"])
        self.assertEqual(student_1.id, payload[0]["student"])
        self.assertEqual(subject.id, payload[0]["subject"])

        self.assertEqual(note_2.asc, payload[1]["asc"])
        self.assertEqual(note_2.final_exam, payload[1]["final_exam"])
        self.assertEqual(note_2.tcp1, payload[1]["tcp1"])
        self.assertEqual(note_2.tcp2, payload[1]["tcp2"])
        self.assertEqual(student_2.id, payload[1]["student"])
        self.assertEqual(subject.id, payload[1]["subject"])

        note_3 = StudentNote.objects.filter(student=student_3).first()
        self.assertIsNotNone(note_3)
        self.assertEqual(note_3.asc, payload[2]["asc"])
        self.assertEqual(note_3.final_exam, payload[2]["final_exam"])
        self.assertEqual(note_3.tcp1, payload[2]["tcp1"])
        self.assertEqual(note_3.tcp2, payload[2]["tcp2"])
        self.assertEqual(student_3.id, payload[2]["student"])
        self.assertEqual(subject.id, payload[2]["subject"])
