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


class TestCreateStudentResponse(StudentTestCase):
    def call_create_student_response(
        self,
        payload: Dict[str, Any],
        unauthorized: bool = False,
        forbidden: bool = False,
        bad_request: bool = False,
        not_found: bool = False,
        print_json_response: bool = False,
    ):
        URL = reverse("student_response-list")
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

    def test_create_student_response(self):
        course = SchoolYear.get_current_course()
        subject = Subject.objects.first()
        subject_section_1 = SubjectSection.objects.create(
            subject=subject,
            index=1,
            title="title_subject_section_2",
            description="description_subject_section_2",
            school_year=course,
        )
        task_section_1 = SchoolTask.objects.create(
            title="title_subject_section_2",
            description="description_subject_section_2",
            date=timezone.now(),
            subject_section=subject_section_1,
        )
        student = self.create_random_student(grade=subject.grade)
        payload = {
            "description": "description",
            "student": student.id,
            "school_task": task_section_1.id,
            "files": [
                {
                    "file": "dir/to/file.txt",
                    "title": "title_file_1",
                    "description": "description_file_1",
                },
                {
                    "file": "dir/to/file2.txt",
                    "title": "title_file_2",
                    "description": "description_file_2",
                },
            ],
        }
        response = self.call_create_student_response(
            payload=payload, print_json_response=False
        )
        q = StudentResponse.objects.filter(student=student)
        self.assertEqual(1, q.count())
        student_response: StudentResponse = q.first()
        self.assertIsNotNone(student_response)
        self.assertEqual("description", student_response.description)
        self.assertEqual(student.id, student_response.student.id)
        self.assertEqual(task_section_1.id, student_response.school_task.id)

        q = FileStudentResponse.objects.filter(
            student_response=student_response
        ).order_by("title")
        self.assertEqual(2, q.count())
        for i, file in enumerate(q):
            file_data = payload["files"][i]
            self.assertEqual(file.title, file_data["title"])
            self.assertEqual(file.description, file_data["description"])
            self.assertEqual(file.file, file_data["file"])
            self.assertEqual(file.type, "TXT")
