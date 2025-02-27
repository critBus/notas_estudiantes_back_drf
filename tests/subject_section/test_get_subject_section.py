from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework.reverse import reverse  # Para generar urls

from apps.project.models import (
    FileFolder,
    FileSchoolTask,
    FileStudentResponse,
    Folder,
    SchoolTask,
    SchoolYear,
    StudentResponse,
    Subject,
    SubjectSection,
)
from tests.student.parent_case.student_test_case import StudentTestCase

User = get_user_model()


class TestGetSubjectSection(StudentTestCase):
    def call_get_subject_section(
        self,
        id: int,
        unauthorized: bool = False,
        forbidden: bool = False,
        bad_request: bool = False,
        not_found: bool = False,
        print_json_response: bool = False,
    ):
        URL = reverse("subject-section-create", args=[id])
        response_dict = self.call_get(
            url=URL,
            unauthorized=unauthorized,
            forbidden=forbidden,
            bad_request=bad_request,
            not_found=not_found,
            print_json_response=print_json_response,
        )

        return response_dict

    def test_get_subject_section(self):
        SubjectSection.objects.all().delete()
        course = SchoolYear.get_current_course()
        subject = Subject.objects.first()
        subject_section_1 = SubjectSection.objects.create(
            subject=subject,
            index=1,
            title="title_subject_section_2",
            description="description_subject_section_2",
            school_year=course,
        )
        subject_section_2 = SubjectSection.objects.create(
            subject=subject,
            index=2,
            title="title_subject_section_2",
            description="description_subject_section_2",
            school_year=course,
        )
        folder_1_section_1 = Folder.objects.create(
            title="folder 1 section 1",
            description="descripcion",
            subject_section=subject_section_1,
        )

        folder_2_section_1 = Folder.objects.create(
            title="folder 2 section 1",
            description="descripcion",
            subject_section=subject_section_1,
        )

        file_folder_1_section_1 = FileFolder.objects.create(
            title="title_subject_section_2",
            description="description_subject_section_2",
            type="TIPO",
            file="/path/to.tipo",
            folder=folder_1_section_1,
        )

        file_folder_2_section_1 = FileFolder.objects.create(
            title="title_subject_section_2",
            description="description_subject_section_2",
            type="TIPO",
            file="/path/to.tipo",
            folder=folder_1_section_1,
        )

        folder_1_section_2 = Folder.objects.create(
            title="folder 2 section 2",
            description="descripcion",
            subject_section=subject_section_2,
        )
        file_folder_1_section_2 = FileFolder.objects.create(
            title="title_subject_section_1",
            description="description_subject_section_2",
            type="TIPO",
            file="/path/to.tipo",
            folder=folder_1_section_2,
        )

        task_section_2 = SchoolTask.objects.create(
            title="title_subject_section_2",
            description="description_subject_section_2",
            date=timezone.now(),
            subject_section=subject_section_2,
        )
        file_task_1_section_2 = FileSchoolTask.objects.create(
            title="title_subject_section_2",
            description="description_subject_section_2",
            type="TIPO",
            file="/path2/to.tipo",
            school_task=task_section_2,
        )
        student_response_section_2 = StudentResponse.objects.create(
            date=timezone.now(),
            description="description_subject_section_2",
            school_task=task_section_2,
        )
        file_student_response_section_2 = FileStudentResponse.objects.create(
            title="title_subject_section_2",
            description="description_subject_section_2",
            student_response=student_response_section_2,
            type="TIPO",
            file="/path2/to.tipo",
        )

        respose_dict = self.call_get_subject_section(
            id=subject.id, print_json_response=False
        )

        self.assertEqual(
            respose_dict,
            [
                {
                    "id": subject_section_1.id,
                    "index": subject_section_1.index,
                    "title": subject_section_1.title,
                    "description": subject_section_1.description,
                    "folders": [
                        {
                            "id": folder_1_section_1.id,
                            "title": folder_1_section_1.title,
                            "description": folder_1_section_1.description,
                            "files": [
                                {
                                    "id": file_folder_1_section_1.id,
                                    "title": file_folder_1_section_1.title,
                                    "description": file_folder_1_section_1.description,
                                    "file": str(file_folder_1_section_1.file),
                                },
                                {
                                    "id": file_folder_2_section_1.id,
                                    "title": file_folder_2_section_1.title,
                                    "description": file_folder_2_section_1.description,
                                    "file": str(file_folder_2_section_1.file),
                                },
                            ],
                        },
                        {
                            "id": folder_2_section_1.id,
                            "title": folder_2_section_1.title,
                            "description": folder_2_section_1.description,
                            "files": [],
                        },
                    ],
                    "tasks": [],
                },
                {
                    "id": subject_section_2.id,
                    "index": subject_section_2.index,
                    "title": subject_section_2.title,
                    "description": subject_section_2.description,
                    "folders": [
                        {
                            "id": folder_1_section_2.id,
                            "title": folder_1_section_2.title,
                            "description": folder_1_section_2.description,
                            "files": [
                                {
                                    "id": file_folder_1_section_2.id,
                                    "title": file_folder_1_section_2.title,
                                    "description": file_folder_1_section_2.description,
                                    "file": str(file_folder_1_section_2.file),
                                }
                            ],
                        }
                    ],
                    "tasks": [
                        {
                            "id": task_section_2.id,
                            "title": task_section_2.title,
                            "description": task_section_2.description,
                            "files": [
                                {
                                    "id": file_task_1_section_2.id,
                                    "title": file_task_1_section_2.title,
                                    "description": file_task_1_section_2.description,
                                    "file": file_task_1_section_2.file,
                                }
                            ],
                            "students_responses": [
                                {
                                    "id": student_response_section_2.id,
                                    "description": student_response_section_2.description,
                                    "files": [
                                        {
                                            "id": file_student_response_section_2.id,
                                            "title": file_student_response_section_2.title,
                                            "description": file_student_response_section_2.description,
                                            "file": file_student_response_section_2.file,
                                        }
                                    ],
                                }
                            ],
                        }
                    ],
                },
            ],
        )
