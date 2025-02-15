from typing import List

from django.db import models


class SchoolYear(models.Model):
    start_date = models.DateField(verbose_name="Fecha de inicio")
    end_date = models.DateField(verbose_name="Fecha de fin")
    name = models.CharField(
        max_length=255, verbose_name="Nombre", help_text="ejemplo: 2024-2025"
    )

    def __str__(self):
        return self.name

    def get_subjects(self, grade: int):
        return Subject.objects.filter(
            studentnote__school_year=self, grade=grade
        )

    @staticmethod
    def get_current_course():
        return SchoolYear.objects.order_by("-start_date").first()


class Student(models.Model):
    ci = models.CharField(max_length=20, verbose_name="Carnet de Identidad")
    address = models.CharField(max_length=255, verbose_name="Dirección")
    grade = models.IntegerField(
        choices=[(7, 7), (8, 8), (9, 9)], verbose_name="Grado"
    )
    last_name = models.CharField(max_length=255, verbose_name="Apellidos")
    first_name = models.CharField(max_length=255, verbose_name="Nombres")
    registration_number = models.CharField(
        max_length=255, verbose_name="Número de Registro"
    )
    sex = models.CharField(max_length=10, verbose_name="Sexo")
    is_graduated = models.BooleanField(default=False, verbose_name="Graduado")
    is_dropped_out = models.BooleanField(verbose_name="Baja")

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name = "Estudiante"
        verbose_name_plural = "Estudiantes"

    def their_notes_are_valid(self, curse=None):
        if not curse:
            curse = SchoolYear.get_current_course()
        subjects = curse.get_subjects(grade=self.grade)
        if not subjects:
            return False
        for subject in subjects:
            notes = StudentNote.objects.filter(
                student=self, subject=subject, school_year=curse
            )
            if not StudentNote.are_valid(notes):
                return False
        return True

    def create_ballot(self, list_career: List[str]):
        StudentCareer.objects.filter(student=self).delete()
        for i, career in enumerate(list_career):
            StudentCareer.objects.create(student=self, index=i, career=career)

    def get_ballot(self):
        return [
            v.name
            for v in StudentCareer.objects.filter(student=self).order_by(
                "index"
            )
        ]


class Dropout(models.Model):
    is_dropped_out = models.BooleanField(verbose_name="Baja")
    date = models.DateField(verbose_name="Fecha")
    municipality = models.CharField(max_length=255, verbose_name="Municipio")
    province = models.CharField(max_length=255, verbose_name="Provincia")
    school = models.CharField(max_length=255, verbose_name="Escuela")
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, verbose_name="Estudiante"
    )

    class Meta:
        verbose_name = "Baja"
        verbose_name_plural = "Bajas"


class Career(models.Model):
    amount = models.IntegerField(verbose_name="Monto")
    name = models.CharField(max_length=255, verbose_name="Nombre")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Carrera"
        verbose_name_plural = "Carreras"


class Graduation(models.Model):
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, verbose_name="Estudiante"
    )
    graduation_number = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Número de Matrícula",
    )
    graduation_date = models.DateField(
        blank=True, null=True, verbose_name="Fecha de Graduación"
    )
    career = models.CharField(
        max_length=255, blank=True, null=True, verbose_name="Carrera"
    )
    ranking_score = models.FloatField(
        blank=True, null=True, verbose_name="Nota Escalafón"
    )
    ranking_number = models.IntegerField(
        blank=True, null=True, verbose_name="Número de Escalafón"
    )

    class Meta:
        verbose_name = "Graduación"
        verbose_name_plural = "Graduaciones"


class GraduationGrade(models.Model):
    subject_name = models.CharField(
        max_length=255, verbose_name="Nombre de Asignatura"
    )
    assignment_grade = models.FloatField(
        blank=True, null=True, verbose_name="Nota de Asignación"
    )
    tcp1 = models.FloatField(blank=True, null=True, verbose_name="TCP1")
    tcp2 = models.FloatField(blank=True, null=True, verbose_name="TCP2")
    final_exam = models.FloatField(
        blank=True, null=True, verbose_name="Examen Final"
    )
    final_grade = models.FloatField(
        blank=True, null=True, verbose_name="Nota Final"
    )
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, verbose_name="Estudiante"
    )

    class Meta:
        verbose_name = "Nota de Graduado"
        verbose_name_plural = "Notas de Graduados"


class Subject(models.Model):
    grade = models.IntegerField(verbose_name="Grado")
    name = models.CharField(max_length=255, verbose_name="Nombre")
    tcp2_required = models.BooleanField(verbose_name="Requiere TCP2")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Asignatura"
        verbose_name_plural = "Asignaturas"


class StudentNote(models.Model):
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, verbose_name="Estudiante"
    )
    subject = models.ForeignKey(
        Subject, on_delete=models.CASCADE, verbose_name="Asignatura"
    )
    acs = models.FloatField(blank=True, null=True, verbose_name="ACS")
    final_grade = models.FloatField(
        blank=True, null=True, verbose_name="Nota Final"
    )
    final_exam = models.FloatField(
        blank=True, null=True, verbose_name="Examen Final"
    )
    tcp1 = models.FloatField(blank=True, null=True, verbose_name="TCP1")
    tcp2 = models.FloatField(blank=True, null=True, verbose_name="TCP2")
    school_year = models.ForeignKey(
        SchoolYear, on_delete=models.CASCADE, verbose_name="Año escolar"
    )

    class Meta:
        verbose_name = "Nota"
        verbose_name_plural = "Notas"

    @staticmethod
    def are_valid(notes):
        # TODO: este metodo es fake aun
        if not notes:
            return False
        return True


class Award(models.Model):
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, verbose_name="Estudiante"
    )
    graduation_year = models.IntegerField(
        blank=True, null=True, verbose_name="Año de Graduación"
    )
    career = models.CharField(
        max_length=255, blank=True, null=True, verbose_name="Carrera"
    )
    ranking_score = models.FloatField(
        blank=True, null=True, verbose_name="Nota Escalafón"
    )
    ranking_number = models.IntegerField(
        blank=True, null=True, verbose_name="Número de Escalafón"
    )

    class Meta:
        verbose_name = "Otorgamiento"
        verbose_name_plural = "Otorgamientos"


class StudentCareer(models.Model):
    career = models.ForeignKey(
        Career, on_delete=models.CASCADE, verbose_name="Carrera"
    )
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, verbose_name="Estudiante"
    )
    index = models.IntegerField(verbose_name="Índice")

    class Meta:
        verbose_name = "Estudiante - Carrera"
        verbose_name_plural = "Estudiantes - Carreras"


class DegreeScale(models.Model):
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, verbose_name="Estudiante"
    )
    school_year = models.ForeignKey(
        SchoolYear, on_delete=models.CASCADE, verbose_name="Año escolar"
    )
    ranking_score = models.FloatField(
        blank=True, null=True, verbose_name="Nota Escalafón"
    )
    ranking_number = models.IntegerField(
        blank=True, null=True, verbose_name="Número de Escalafón"
    )

    class Meta:
        verbose_name = "Escalafón Estudiantil"
        verbose_name_plural = "Escalafones Estudiantiles"
