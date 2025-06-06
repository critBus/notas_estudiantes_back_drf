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


class TestGetResponsesOfTask(StudentTestCase):
    def call_get_responses_of_task(
        self,
        id: int,
        unauthorized: bool = False,
        forbidden: bool = False,
        bad_request: bool = False,
        not_found: bool = False,
        print_json_response: bool = False,
    ):
        URL = reverse("subject-section-responses", args=[id])
        response_dict = self.call_get(
            url=URL,
            unauthorized=unauthorized,
            forbidden=forbidden,
            bad_request=bad_request,
            not_found=not_found,
            print_json_response=print_json_response,
        )

        return response_dict

    def test_get_taks_of_section(self):
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

        respose_dict = self.call_get_responses_of_task(
            id=task_section.id, print_json_response=False
        )

        self.assertEqual(
            respose_dict,
            [
                {
                    "id": student_response_section.id,
                    "student": {
                        "id": student.id,
                        "is_approved": False,
                        "ci": student.ci,
                        "address": student.address,
                        "grade": student.grade,
                        "last_name": student.last_name,
                        "first_name": student.first_name,
                        "registration_number": student.registration_number,
                        "sex": student.sex,
                        "is_graduated": False,
                        "is_dropped_out": False,
                        "user": None,
                        "group": None,
                        "can_edit_bullet": False,
                    },
                    "description": student_response_section.description,
                    "files": [
                        {
                            "id": file_student_response_section.id,
                            "title": file_student_response_section.title,
                            "description": file_student_response_section.description,
                            "file": file_student_response_section.file,
                        }
                    ],
                    "subject_id": subject.id,
                }
            ],
        )
