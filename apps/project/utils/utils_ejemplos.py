import random
from datetime import timedelta

from django.utils import timezone

from apps.project.models import (
    Career,
    DegreeScale,
    Dropout,
    GrantCareer,
    SchoolYear,
    Student,
    StudentCareer,
)
from tests.professor.mixin.professor_mixin import ProfessorMixin
from tests.student.mixin.school_year_mixin import SchoolYearMixin
from tests.student.mixin.student_mixin import StudentMixin
from tests.student.mixin.subject_mixin import SubjectMixin
from tests.utils.mixin.user_mixin import UserMixin


class Factory(
    UserMixin, SubjectMixin, SchoolYearMixin, StudentMixin, ProfessorMixin
):
    def crear_carreras(self):
        self.careers = []
        careers_names = [f"career{i}" for i in range(20)]
        for name in careers_names:
            career = Career.objects.create(
                name=name, amount=random.randint(1, 5)
            )
            self.careers.append(career)

    def add_ballot_to_student(
        self,
        student: Student,
        initial_index: int = 0,
        amount_to_agregate: int = 10,
    ):
        for i in range(amount_to_agregate):
            index = (10 - amount_to_agregate) + i + 1
            StudentCareer.objects.create(
                student=student,
                career=self.careers[initial_index + i],
                index=index,
            )


def crear_datos_random():
    if Student.objects.count() == 0:
        print("Cargando datos de ejemplo ...")
        factory = Factory()
        factory.create_current_school_year()
        factory.crear_asignaturas()
        factory.crear_carreras()

        students_7 = []
        students_8 = []
        students_9 = []
        for i in range(random.randint(27, 40)):
            student_7 = factory.create_random_student(grade=7)
            students_7.append(student_7)

            student_8 = factory.create_random_student(grade=8)
            students_8.append(student_8)

            student_9 = factory.create_random_student(grade=9)
            students_9.append(student_9)

            baja = random.randint(1, 20) == 1
            if baja:
                for student in [student_7, student_8, student_9]:
                    Dropout.objects.create(
                        student=student,
                        date=timezone.now(),
                        municipality=random.choice(
                            ["Jaruco", "Santa Cruz", "San Jose", "Guines"]
                        ),
                        province=random.choice(
                            [
                                "Mayabeque",
                                "La Habana",
                                "Pinar del Rio",
                                "Granma",
                            ]
                        ),
                        school=random.choice(
                            ["Giteras", "Pedron", "Juilo Soler"]
                        ),
                    )

            aprobar = random.randint(1, 15) > 3
            if aprobar:
                factory.ponerle_notas_validas_al_estudiante(student_7)
                factory.ponerle_notas_validas_al_estudiante(student_8)
                factory.ponerle_notas_validas_al_estudiante(student_9)

            if not baja:
                factory.add_ballot_to_student(student_9, i % 10)

        DegreeScale.calculate_all_ranking_number()
        GrantCareer.grant()
        Student.upgrading_7_8_all(grade=8)
        Student.upgrading_7_8_all(grade=7)

        students_9 = [student for student in students_8]
        students_8 = [student for student in students_7]
        students_7 = []

        course: SchoolYear = SchoolYear.get_current_course()
        SchoolYear.objects.create(
            start_date=course.start_date + timedelta(days=365),
            end_date=course.end_date + timedelta(days=365),
            name="2026-2027",
        )

        for i in range(random.randint(27, 40)):
            student_7 = factory.create_random_student(grade=7)
            students_7.append(student_7)
            aprobar = random.randint(1, 15) > 3
            if aprobar:
                factory.ponerle_notas_validas_al_estudiante(student_7)

        for i, student in enumerate(students_9):
            student.refresh_from_db()
            # print(f"grado del estudiante: {student.grade}")
            factory.ponerle_notas_validas_al_estudiante(student)
            factory.add_ballot_to_student(student, i % 10)

        for i, student in enumerate(students_8):
            student.refresh_from_db()
            factory.ponerle_notas_validas_al_estudiante(student)

        for i, student in enumerate(students_7):
            student.refresh_from_db()
            factory.ponerle_notas_validas_al_estudiante(student)

        DegreeScale.calculate_all_ranking_number()

        print("datos cargados")
