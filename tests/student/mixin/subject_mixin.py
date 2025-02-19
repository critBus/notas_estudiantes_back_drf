import random

from apps.project.models import SchoolYear, Student, StudentNote, Subject
from tests.student.mixin.student_mixin import StudentMixin


class SubjectMixin(StudentMixin):
    def crear_asignaturas(self):
        self.subjects = []
        for grade in [7, 8, 9]:
            for name in ["Math", "English", "Cience"]:
                self.subjects.append(
                    Subject.objects.create(
                        grade=grade, name=f"{name}_{grade}", tcp2_required=False
                    )
                )

    def ponerle_notas_validas_al_estudiante(self, student: Student):
        curso = SchoolYear.get_current_course()
        asignaturas = curso.get_subjects(grade=student.grade)
        for asignatura in asignaturas:
            nota = StudentNote.objects.filter(
                subject=asignatura, student=student, school_year=curso
            ).first()
            if not nota:
                nota = StudentNote.objects.create(
                    subject=asignatura, student=student, school_year=curso
                )
            nota.tcp1 = random.randint(60, 100)
            nota.tcp2 = random.randint(60, 100)
            nota.asc = random.randint(6, 10)
            nota.final_exam = random.randint(60, 100)
            nota.calculate_final_grade()
            nota.save()
