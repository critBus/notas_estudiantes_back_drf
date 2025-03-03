from typing import Any, Dict

from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework.reverse import reverse  # Para generar urls

from apps.project.models import (
    FileStudentResponse,
    SchoolTask,
    SchoolYear,
    StudentResponse,
    Subject,
    SubjectSection,
)
from tests.student.parent_case.student_test_case import StudentTestCase

User = get_user_model()


class TestUpdateStudentResponse(StudentTestCase):
    def call_update_student_response(
        self,
        id: int,
        payload: Dict[str, Any],
        unauthorized: bool = False,
        forbidden: bool = False,
        bad_request: bool = False,
        not_found: bool = False,
        print_json_response: bool = False,
    ):
        URL = reverse("student_response-detail", args=[id])
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

    def test_update_student_response(self):
        SubjectSection.objects.all().delete()
        course = SchoolYear.get_current_course()
        subject = Subject.objects.first()
        subject_section = SubjectSection.objects.create(
            subject=subject,
            index=1,
            title="title_subject_section",
            description="description_subject_section",
            school_year=course,
        )
        task_section = SchoolTask.objects.create(
            title="title_subject_section",
            description="description_subject_section",
            date=timezone.now(),
            subject_section=subject_section,
        )
        student = self.create_random_student()
        student_response_section = StudentResponse.objects.create(
            date=timezone.now(),
            description="description_subject_section",
            school_task=task_section,
            student=student,
        )
        file_student_response_section = FileStudentResponse.objects.create(
            title="title_subject_section",
            description="description_subject_section",
            student_response=student_response_section,
            type="TIPO",
            file="/path2/to.tipo",
        )
        payload = {
            "files": [
                {
                    "id": file_student_response_section.id,
                    "file": "edit_file",
                    "title": "edit_title",
                    "description": "edit_description",
                },
                {
                    "file": "new_file",
                    "title": "new_title",
                    "description": "new_description",
                },
            ],
            "description": "edit",
        }
        self.call_update_student_response(
            id=student_response_section.id, payload=payload
        )
        files = FileStudentResponse.objects.filter(
            student_response=student_response_section
        ).order_by("pk")
        self.assertEqual(2, files.count())
        file_old = FileStudentResponse.objects.filter(
            id=file_student_response_section.id
        ).first()
        self.assertIsNotNone(file_old)
        self.assertEqual(file_old.file, payload["files"][0]["file"])
        self.assertEqual(file_old.title, payload["files"][0]["title"])
        self.assertEqual(
            file_old.description, payload["files"][0]["description"]
        )

        file_new = FileStudentResponse.objects.exclude(
            id=file_student_response_section.id
        ).first()
        self.assertIsNotNone(file_new)
        self.assertEqual(file_new.file, payload["files"][1]["file"])
        self.assertEqual(file_new.title, payload["files"][1]["title"])
        self.assertEqual(
            file_new.description, payload["files"][1]["description"]
        )

        payload = {
            "files": [
                {
                    "id": file_new.id,
                    "file": "new_file_edit",
                    "title": "new_title",
                    "description": "new_description",
                }
            ],
            "description": "edit",
        }
        self.call_update_student_response(
            id=student_response_section.id, payload=payload
        )
        files = FileStudentResponse.objects.filter(
            student_response=student_response_section
        ).order_by("pk")
        self.assertEqual(1, files.count())
        file_old = FileStudentResponse.objects.filter(
            id=file_student_response_section.id
        ).first()
        self.assertIsNone(file_old)
        file_new = FileStudentResponse.objects.filter(id=file_new.id).first()
        self.assertIsNotNone(file_new)
        self.assertEqual(file_new.file, payload["files"][0]["file"])
        self.assertEqual(file_new.title, payload["files"][0]["title"])
        self.assertEqual(
            file_new.description, payload["files"][0]["description"]
        )
