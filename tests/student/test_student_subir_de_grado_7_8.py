from django.contrib.auth import get_user_model
from rest_framework.reverse import reverse  # Para generar urls

from apps.project.models import ApprovedSchoolCourse, Student
from tests.student.parent_case.student_test_case import StudentTestCase

User = get_user_model()


class TestStudentSubirDeGrado_7_8(StudentTestCase):
    # def setUp(self):
    #     self.student = self.create_random_student(grade=7)
    def call_subir_de_grado(
        self,
        entity_id: int,
        unauthorized: bool = False,
        forbidden: bool = False,
        bad_request: bool = False,
        not_found: bool = False,
        print_json_response: bool = False,
    ):
        URL = reverse("upgrading7and8", args=[entity_id])
        response_dict = self.call_get(
            url=URL,
            unauthorized=unauthorized,
            forbidden=forbidden,
            bad_request=bad_request,
            not_found=not_found,
            print_json_response=print_json_response,
        )

        return response_dict

    def test_subir_de_grado_7_8(self):
        student = self.create_random_student(grade=7)
        self.call_subir_de_grado(
            entity_id=student.id,
            bad_request=True,
            print_json_response=False,
        )
        self.assertEqual(0, ApprovedSchoolCourse.objects.count())

        self.ponerle_notas_validas_al_estudiante(student=student)
        self.call_subir_de_grado(
            entity_id=student.id,
            bad_request=False,
            print_json_response=False,
        )
        student.refresh_from_db()
        self.assertEqual(student.grade, 8)
        self.assertEqual(1, ApprovedSchoolCourse.objects.count())
        self.assertTrue(
            ApprovedSchoolCourse.objects.filter(
                student=student, grade=7
            ).exists()
        )

        self.ponerle_notas_validas_al_estudiante(student=student)
        self.call_subir_de_grado(
            entity_id=student.id,
            print_json_response=False,
        )
        student.refresh_from_db()
        self.assertEqual(student.grade, 9)
        self.assertEqual(2, ApprovedSchoolCourse.objects.count())
        self.assertTrue(
            ApprovedSchoolCourse.objects.filter(
                student=student, grade=8
            ).exists()
        )

    def test_subir_de_grado_7_all(self):
        students = [self.create_random_student(grade=7) for _ in range(3)]
        for student in students:
            self.ponerle_notas_validas_al_estudiante(student=student)
        Student.upgrading_7_8_all(grade=7)
        self.assertEqual(3, ApprovedSchoolCourse.objects.count())
        for student in students:
            student.refresh_from_db()
            self.assertEqual(student.grade, 8)
            self.assertTrue(
                ApprovedSchoolCourse.objects.filter(
                    student=student, grade=7
                ).exists()
            )
