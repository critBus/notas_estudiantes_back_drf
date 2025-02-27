from typing import Any, Dict

from django.contrib.auth import get_user_model
from rest_framework.reverse import reverse  # Para generar urls

from apps.project.models import (
    FileFolder,
    FileSchoolTask,
    Folder,
    SchoolTask,
    Subject,
    SubjectSection,
)
from tests.student.parent_case.student_test_case import StudentTestCase

User = get_user_model()


class TestCreateSubjectSection(StudentTestCase):
    def call_create_subject_section(
        self,
        id: int,
        payload: Dict[str, Any],
        unauthorized: bool = False,
        forbidden: bool = False,
        bad_request: bool = False,
        not_found: bool = False,
        print_json_response: bool = False,
    ):
        URL = reverse("subject-section-create", args=[id])
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

    def test_degree_scale(self):
        subject = Subject.objects.first()
        data = [
            {
                "index": 2147483647,
                "title": "secciontest",
                "description": "string",
                "folders": [
                    {
                        "title": "string",
                        "description": "string",
                        "files": [
                            {
                                "title": "string",
                                "description": "string",
                                "file": "string",
                            }
                        ],
                    }
                ],
                "tasks": [
                    {
                        "title": "string",
                        "description": "string",
                        "files": [
                            {
                                "title": "string",
                                "description": "string",
                                "file": "string",
                            }
                        ],
                    }
                ],
            }
        ]
        self.call_create_subject_section(id=subject.id, payload=data)
        section = SubjectSection.objects.filter(title="secciontest").first()
        self.assertIsNotNone(section)
        folders = Folder.objects.filter(subject_section=section)
        self.assertEqual(1, folders.count())
        files = FileFolder.objects.filter(folder=folders.first())
        self.assertEqual(1, files.count())
        tasks = SchoolTask.objects.filter(subject_section=section)
        self.assertEqual(1, tasks.count())
        files_tasks = FileSchoolTask.objects.filter(school_task=tasks.first())
        self.assertEqual(1, files_tasks.count())
