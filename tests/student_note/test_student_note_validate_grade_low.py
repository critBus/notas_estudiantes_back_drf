from typing import Any, Dict

from django.contrib.auth import get_user_model
from rest_framework.reverse import reverse  # Para generar urls

from apps.project.models import (
    SchoolYear,
    StudentNote,
)
from tests.student.parent_case.student_test_case import StudentTestCase

User = get_user_model()


class TestStudentNoteValidateLowerGrade(StudentTestCase):
    def call_create_student_note(
        self,
        payload: Dict[str, Any],
        unauthorized: bool = False,
        forbidden: bool = False,
        bad_request: bool = False,
        not_found: bool = False,
        print_json_response: bool = False,
    ):
        URL = reverse("student_note-list")
        response_dict = self.call_create(
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

    def call_update_student_note(
        self,
        id: int,
        payload: Dict[str, Any],
        unauthorized: bool = False,
        forbidden: bool = False,
        bad_request: bool = False,
        not_found: bool = False,
        print_json_response: bool = False,
    ):
        URL = reverse("student_note-detail", args=[id])
        response_dict = self.call_update(
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

    def test_create_student_note_validate_grade_lower(self):
        course = SchoolYear.get_current_course()
        subject = self.subjects[0]
        subject.grade = 9
        subject.save()
        student = self.create_random_student(grade=8)
        self.call_create_student_note(
            payload={
                "asc": 65,
                "final_exam": 45,
                "tcp1": 34,
                "tcp2": 31,
                "student": student.id,
                "subject": subject.id,
                "school_year": course.id,
            },
            print_json_response=False,
            bad_request=True,
        )

        subject.grade = 8
        subject.save()
        self.call_create_student_note(
            payload={
                "asc": 65,
                "final_exam": 45,
                "tcp1": 34,
                "tcp2": 31,
                "student": student.id,
                "subject": subject.id,
                "school_year": course.id,
            },
            print_json_response=False,
        )

    def test_student_note_validate_update_grade_lower(self):
        course = SchoolYear.get_current_course()
        subject_1 = self.subjects[0]
        subject_1.grade = 7
        subject_1.save()
        subject_2 = self.subjects[1]
        subject_2.grade = 8
        subject_2.save()
        subject_3 = self.subjects[2]
        subject_3.grade = 9
        subject_3.save()
        student = self.create_random_student(grade=8)
        note_1 = StudentNote.objects.create(
            subject=subject_1,
            student=student,
            school_year=course,
            asc=7,
            final_exam=11,
            final_grade=21,
            tcp1=21,
            tcp2=21,
        )

        self.call_update_student_note(
            id=note_1.id,
            payload={
                "asc": 65,
                "final_exam": 45,
                "tcp1": 34,
                "tcp2": 31,
                "student": student.id,
                "subject": subject_3.id,
                "school_year": course.id,
            },
            bad_request=True,
            print_json_response=False,
        )
        self.call_update_student_note(
            id=note_1.id,
            payload={
                "asc": 65,
                "final_exam": 45,
                "tcp1": 34,
                "tcp2": 31,
                "student": student.id,
                "subject": subject_2.id,
                "school_year": course.id,
            },
            bad_request=False,
        )
