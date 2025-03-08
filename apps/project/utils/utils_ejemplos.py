import random
from datetime import timedelta

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.utils import timezone
from django.utils.datetime_safe import datetime

User = get_user_model()
from apps.project.models import (
    ROL_NAME_PROFESSOR,
    ROL_NAME_SECRETARY,
    ROL_NAME_STUDENT,
    Career,
    DegreeScale,
    Dropout,
    FileFolder,
    FileSchoolTask,
    FileStudentResponse,
    Folder,
    GrantCareer,
    SchoolEvent,
    SchoolTask,
    SchoolYear,
    Student,
    StudentCareer,
    StudentGroup,
    StudentResponse,
    Subject,
    SubjectSection,
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

        course_old: SchoolYear = SchoolYear.get_current_course()
        course = SchoolYear.objects.create(
            start_date=course_old.start_date + timedelta(days=365),
            end_date=course_old.end_date + timedelta(days=365),
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

        print("crear secciones ...")
        professors = []
        for subject in Subject.objects.all():
            professor = factory.create_random_professor()
            subject.professor.add(professor)
            professors.append(professor)

            subject_section_1 = SubjectSection.objects.create(
                subject=subject,
                index=1,
                title="Primera Semana ",
                description="primeras clases",
                school_year=course,
            )
            subject_section_2 = SubjectSection.objects.create(
                subject=subject,
                index=2,
                title="Segunda Semana",
                description="mas clases",
                school_year=course,
            )
            folder_1_section_1 = Folder.objects.create(
                title="Bibliografia",
                description="todo lo necesario",
                subject_section=subject_section_1,
            )

            Folder.objects.create(
                title="Libros",
                description="lo necesitas",
                subject_section=subject_section_1,
            )

            FileFolder.objects.create(
                title="Libro 1",
                description="Es interesante",
                type="TIPO",
                file="/path/to.tipo",
                folder=folder_1_section_1,
            )

            FileFolder.objects.create(
                title="Libro 1",
                description="lo quieres",
                type="TIPO",
                file="/path/to.tipo",
                folder=folder_1_section_1,
            )

            folder_1_section_2 = Folder.objects.create(
                title="Archivos Necesarios",
                description="utilizalos",
                subject_section=subject_section_2,
            )
            FileFolder.objects.create(
                title="Ejmplo",
                description="miralo",
                type="TIPO",
                file="/path/to.tipo",
                folder=folder_1_section_2,
            )

            task_section_2 = SchoolTask.objects.create(
                title="Tarea para esta semana",
                description="tienen que aprobar",
                date=timezone.now(),
                subject_section=subject_section_2,
            )
            FileSchoolTask.objects.create(
                title="La tarea",
                description="esta dificil",
                type="TIPO",
                file="/path2/to.tipo",
                school_task=task_section_2,
            )
            for student in Student.objects.filter(
                grade=subject.grade, is_graduated=False, is_dropped_out=False
            ):
                student_response_section_2 = StudentResponse.objects.create(
                    date=timezone.now(),
                    description="esta es mi respuesta",
                    school_task=task_section_2,
                    student=student,
                )
                (
                    FileStudentResponse.objects.create(
                        title="Archivo de mi respuesta",
                        description="Me esforce",
                        student_response=student_response_section_2,
                        type="TIPO",
                        file="/path2/to.tipo",
                    )
                )
        print("crear eventos ...")
        events_data = [
            {
                "title": "Día del Deporte",
                "description": "Competencias deportivas y actividades recreativas.",
            },
            {
                "title": "Feria de Ciencias",
                "description": "Exposición de proyectos científicos realizados por los estudiantes.",
            },
            {
                "title": "Concierto de Primavera",
                "description": "Presentaciones musicales de los estudiantes.",
            },
            {
                "title": "Día de la Lectura",
                "description": "Actividades para fomentar la lectura y el amor por los libros.",
            },
            {
                "title": "Excursión al Museo",
                "description": "Visita guiada al museo local para aprender sobre la historia.",
            },
            {
                "title": "Taller de Arte",
                "description": "Clases de pintura y manualidades para todos los niveles.",
            },
            {
                "title": "Día de la Familia",
                "description": "Actividades para involucrar a las familias en la vida escolar.",
            },
            {
                "title": "Competencia de Matemáticas",
                "description": "Concurso de habilidades matemáticas para estudiantes.",
            },
            {
                "title": "Festival de Cine",
                "description": "Proyección de cortometrajes realizados por los estudiantes.",
            },
            {
                "title": "Día del Medio Ambiente",
                "description": "Actividades para promover la conciencia ambiental.",
            },
        ]

        print("Creando Eventos ...")
        # Año actual
        current_year = timezone.now().year

        for event_data in events_data:
            # Generar una fecha aleatoria en el año actual
            start_date = datetime(current_year, 1, 1)
            end_date = datetime(current_year, 12, 31)
            random_date = start_date + timedelta(
                days=random.randint(0, (end_date - start_date).days)
            )

            # Crear el evento
            SchoolEvent.objects.create(
                date=random_date,
                title=event_data["title"],
                description=event_data["description"],
            )

        print("Creando cuentas por defecto ...")
        secretary: User = User.objects.create_user(
            username="secretaria", password="123", email="estudiante@test.com"
        )
        secretary.groups.add(
            Group.objects.filter(name=ROL_NAME_SECRETARY).first()
        )

        student_user = User.objects.create_user(
            username="estudiante", password="123", email="estudiante@test.com"
        )
        factory.create_random_student(user=student_user, grade=7)
        student_user.groups.add(
            Group.objects.filter(name=ROL_NAME_STUDENT).first()
        )

        professor_user = User.objects.create_user(
            username="profesor", password="123", email="profesor@test.com"
        )
        professor_user.groups.add(
            Group.objects.filter(name=ROL_NAME_PROFESSOR).first()
        )
        professor_account = factory.create_random_professor(user=professor_user)

        for subject in Subject.objects.all():
            subject.professor.add(professor_account)

        print("Creando profesores ...")
        group_7_1 = StudentGroup.objects.create(
            name="7MO1",
            grade=7,
        )
        group_7_1.professors.add(professors[0])
        middle = int(len(students_7) / 2)
        for student in students_7[:middle]:
            student.refresh_from_db()
            student.group = group_7_1
            student.save()

        group_7_2 = StudentGroup.objects.create(
            name="7MO2",
            grade=7,
        )
        for student in students_7[middle:]:
            student.refresh_from_db()
            student.group = group_7_2
            student.save()

        group_8_1 = StudentGroup.objects.create(
            name="8MO1",
            grade=8,
        )
        group_8_1.professors.add(professors[2])
        middle = int(len(students_8) / 2)
        for student in students_8[:middle]:
            student.refresh_from_db()
            student.group = group_8_1
            student.save()

        group_8_2 = StudentGroup.objects.create(
            name="8MO2",
            grade=8,
        )
        group_8_2.professors.add(professors[3])
        for student in students_8[middle:]:
            student.refresh_from_db()
            student.group = group_8_2
            student.save()

        group_9_1 = StudentGroup.objects.create(
            name="9MO1",
            grade=9,
        )
        group_9_1.professors.add(professors[4])
        middle = int(len(students_9) / 2)
        for student in students_9[:middle]:
            student.refresh_from_db()
            student.group = group_9_1
            student.save()

        group_9_2 = StudentGroup.objects.create(
            name="9MO2",
            grade=9,
        )
        group_9_2.professors.add(professors[5])
        for student in students_9[middle:]:
            student.refresh_from_db()
            student.group = group_9_2
            student.save()
        print("datos cargados")
