from django.contrib.auth import get_user_model

from apps.project.models import (
    FileFolder,
    FileSchoolTask,
    Folder,
    SchoolTask,
    Subject,
    SubjectSection,
)
from tests.subject_section.parent_case.subject_section_test_case import (
    SubjectSectionTestCase,
)

User = get_user_model()


class TestCreateSubjectSection(SubjectSectionTestCase):
    def test_create_subject_section(self):
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
        folder = folders.first()
        files = FileFolder.objects.filter(folder=folder)
        self.assertEqual(1, files.count())
        file_folder = files.first()
        tasks = SchoolTask.objects.filter(subject_section=section)
        self.assertEqual(1, tasks.count())
        task = tasks.first()
        files_tasks = FileSchoolTask.objects.filter(school_task=task)
        file_task = files_tasks.first()
        self.assertEqual(1, files_tasks.count())

        data = [
            {
                "id": section.id,
                "index": 2,
                "title": "secciontestedit",
                "description": "stringedit",
                "folders": [
                    {
                        "id": folder.id,
                        "title": "string2",
                        "description": "string2",
                        "files": [
                            {
                                "id": file_folder.id,
                                "title": "string2",
                                "description": "string2",
                                "file": "string2",
                            }
                        ],
                    },
                    {
                        "title": "string3",
                        "description": "string3",
                        "files": [
                            {
                                "title": "string2",
                                "description": "string2",
                                "file": "string2",
                            },
                            {
                                "title": "string2",
                                "description": "string2",
                                "file": "string2",
                            },
                        ],
                    },
                ],
                "tasks": [
                    {
                        "id": task.id,
                        "title": "string",
                        "description": "string",
                        "files": [
                            {
                                "id": file_task.id,
                                "title": "string",
                                "description": "string",
                                "file": "string",
                            },
                            {
                                "title": "string2",
                                "description": "string2",
                                "file": "string2",
                            },
                        ],
                    }
                ],
            }
        ]

        old_id = section.id
        self.call_create_subject_section(id=subject.id, payload=data)
        section = SubjectSection.objects.filter(id=old_id).first()
        self.assertIsNotNone(section)
        folders = Folder.objects.filter(subject_section=section).order_by(
            "title"
        )
        self.assertEqual(2, folders.count())
        folder = Folder.objects.filter(id=folder.id).first()
        self.assertIsNotNone(folder)
        file = FileFolder.objects.filter(id=file_folder.id).first()
        self.assertIsNotNone(file)
        files = FileFolder.objects.filter(folder=folders.first())
        self.assertEqual(1, files.count())
        tasks = SchoolTask.objects.filter(subject_section=section)
        self.assertEqual(1, tasks.count())
        task = SchoolTask.objects.filter(id=task.id).first()
        self.assertIsNotNone(task)
        task = tasks.first()
        files_tasks = FileSchoolTask.objects.filter(school_task=task)
        self.assertEqual(2, files_tasks.count())
