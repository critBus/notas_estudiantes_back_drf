from typing import Dict, List

from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone
from rest_framework import serializers

from apps.project.utils.consts import AMOUNT_OF_CAREER_ON_BALLOT

User = get_user_model()
GRADES_CHOICES = [(7, 7), (8, 8), (9, 9)]
ROL_NAME_ADMIN = "admin"
ROL_NAME_STUDENT = "estudiante"
ROL_NAME_PROFESSOR = "professor"
ROL_NAME_SECRETARY = "secretary"


class SchoolYear(models.Model):
    start_date = models.DateField(verbose_name="Fecha de inicio")
    end_date = models.DateField(verbose_name="Fecha de fin")
    name = models.CharField(
        max_length=255,
        verbose_name="Nombre",
        help_text="ejemplo: 2024-2025",
        unique=True,
    )

    def __str__(self):
        return self.name

    def get_subjects(self, grade: int):
        return Subject.objects.filter(grade=grade)

    def get_previus_course(self):
        previus_course = None
        for course in SchoolYear.objects.order_by("start_date"):
            if previus_course is not None:
                if course.id == self.id:
                    break
            previus_course = course
        return previus_course

    @staticmethod
    def get_current_course():
        return SchoolYear.objects.order_by("-start_date").first()


class Professor(models.Model):
    ci = models.CharField(
        max_length=20, verbose_name="Carnet de Identidad", unique=True
    )
    address = models.CharField(max_length=255, verbose_name="Dirección")
    last_name = models.CharField(max_length=255, verbose_name="Apellidos")
    first_name = models.CharField(max_length=255, verbose_name="Nombres")
    sex = models.CharField(
        max_length=10,
        verbose_name="Sexo",
        choices=[("F", "Femenino"), ("M", "Masculino")],
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Cuenta",
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "Profesor"
        verbose_name_plural = "Profesores"

    def save(self, *args, **kwargs):
        if self.user:
            self.user.first_name = self.first_name
            self.user.last_name = self.last_name
            self.user.save()
        return super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.user:
            self.user.delete()
            self.user = None
        return super().delete(*args, **kwargs)


class StudentGroup(models.Model):
    name = models.CharField(max_length=255, verbose_name="Nombre")
    grade = models.IntegerField(choices=GRADES_CHOICES, verbose_name="Grado")
    professors = models.ManyToManyField(Professor, verbose_name="Profesores")

    class Meta:
        verbose_name = "Grupo de Estudiante"
        verbose_name_plural = "Grupos de Estudiantes"


class Student(models.Model):
    ci = models.CharField(
        max_length=20, verbose_name="Carnet de Identidad", unique=True
    )
    address = models.CharField(max_length=255, verbose_name="Dirección")
    grade = models.IntegerField(choices=GRADES_CHOICES, verbose_name="Grado")
    last_name = models.CharField(max_length=255, verbose_name="Apellidos")
    first_name = models.CharField(max_length=255, verbose_name="Nombres")
    registration_number = models.CharField(
        max_length=255, verbose_name="Número de Registro"
    )
    sex = models.CharField(
        max_length=10,
        verbose_name="Sexo",
        choices=[("F", "Femenino"), ("M", "Masculino")],
    )
    is_graduated = models.BooleanField(default=False, verbose_name="Graduado")
    is_dropped_out = models.BooleanField(default=False, verbose_name="Baja")
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        verbose_name="Cuenta",
        blank=True,
        null=True,
    )
    group = models.ForeignKey(
        StudentGroup,
        on_delete=models.SET_NULL,
        verbose_name="Grupo",
        blank=True,
        null=True,
    )
    can_edit_bullet = models.BooleanField(
        default=False, verbose_name="Puede Editar Su Boleta"
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name = "Estudiante"
        verbose_name_plural = "Estudiantes"

    def save(self, *args, **kwargs):
        if self.user:
            self.user.first_name = self.first_name
            self.user.last_name = self.last_name
            self.user.save()
        return super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.user:
            self.user.delete()
            self.user = None
        return super().delete(*args, **kwargs)

    def has_career_awarded(self):
        return GrantCareer.objects.filter(student=self).exists()

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
            v.career.name
            for v in StudentCareer.objects.filter(student=self).order_by(
                "index"
            )
        ]

    def has_ballot(self) -> bool:
        count = StudentCareer.objects.filter(student=self).count()
        return count == AMOUNT_OF_CAREER_ON_BALLOT

    def upgrading_7_8(self, today=None) -> bool:
        grade = self.grade
        if grade not in [7, 8]:
            raise serializers.ValidationError("El grado tiene que ser 7 o 8")
        if today is None:
            today = timezone.now().date()
        course = SchoolYear.get_current_course()
        if self.their_notes_are_valid():
            self.grade += 1
            self.save()
            if not ApprovedSchoolCourse.objects.filter(
                student=self, grade=grade
            ).exists():
                ApprovedSchoolCourse.objects.create(
                    student=self,
                    school_year=course,
                    date=today,
                    grade=grade,
                )
            return True
        return False

    @staticmethod
    def graduate_all(today=None):
        if today is None:
            today = timezone.now().date()
        school_year = SchoolYear.get_current_course()
        students_9 = Student.get_students_current_9()
        graduate_students = []
        for student in students_9:
            if student.has_career_awarded():
                student.is_graduated = True
                student.save()

                approved_school_course = ApprovedSchoolCourse.objects.filter(
                    student=student, grade=9
                ).first()
                if not approved_school_course:
                    ApprovedSchoolCourse.objects.create(
                        student=student,
                        school_year=school_year,
                        date=today,
                        grade=9,
                    )
                graduate_students.append(student)
        return graduate_students

    @staticmethod
    def upgrading_7_8_all(grade=7, today=None):
        if grade not in [7, 8]:
            raise serializers.ValidationError("El grado tiene que ser 7 o 8")
        if today is None:
            today = timezone.now().date()
        students = Student.objects.filter(
            is_graduated=False, is_dropped_out=False, grade=grade
        )
        upgrading_students = []
        for student in students:
            if student.upgrading_7_8(today=today):
                upgrading_students.append(student)
        return upgrading_students

    @staticmethod
    def get_students_current_9():
        return Student.objects.filter(
            is_graduated=False, is_dropped_out=False, grade=9
        )

    @staticmethod
    def are_missing_ballots():
        q = Student.get_students_current_9()
        if q.count() == 0:
            return True
        count_with_notes_valid = 0
        for student in q:
            if student.their_notes_are_valid():
                count_with_notes_valid += 1
                if not student.has_ballot():
                    return True
        return count_with_notes_valid == 0

    @staticmethod
    def get_students_without_ballots():
        q = Student.get_students_current_9()
        students_without_ballots = []
        for student in q:
            if not student.has_ballot():  # student.their_notes_are_valid() and
                students_without_ballots.append(student)
        return students_without_ballots


class ApprovedSchoolCourse(models.Model):
    date = models.DateField(verbose_name="Fecha")
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, verbose_name="Estudiante"
    )
    grade = models.IntegerField(verbose_name="Grado", choices=GRADES_CHOICES)
    school_year = models.ForeignKey(
        SchoolYear, on_delete=models.CASCADE, verbose_name="Año escolar"
    )

    class Meta:
        verbose_name = "Curso Escolar Aprobado"
        verbose_name_plural = "Cursos Escolares Aprobados"


class Dropout(models.Model):
    date = models.DateField(verbose_name="Fecha")
    municipality = models.CharField(max_length=255, verbose_name="Municipio")
    province = models.CharField(max_length=255, verbose_name="Provincia")
    school = models.CharField(max_length=255, verbose_name="Escuela")
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        verbose_name="Estudiante",
        unique=True,
    )
    is_dropout = models.BooleanField(verbose_name="Es Baja", default=True)

    class Meta:
        verbose_name = "Baja"
        verbose_name_plural = "Bajas"

    def save(self, *args, **kwargs):
        es_nuevo = self.pk is None
        if not es_nuevo:
            old: Dropout = Dropout.objects.filter(
                id=self.id, is_dropout=True
            ).first()
            if old:
                if old.student != self.student:
                    old.student.is_dropped_out = False
                    old.student.save()
                elif old.is_dropout and not self.is_dropout:
                    old.student.is_dropped_out = False
                    old.student.save()

        if self.student and self.is_dropout:
            self.student.is_dropped_out = True
            self.student.save()
        return super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.student:
            self.student.is_dropped_out = False
            self.student.save()
        return super().delete(*args, **kwargs)


class Career(models.Model):
    amount = models.IntegerField(verbose_name="Monto")
    name = models.CharField(max_length=255, verbose_name="Nombre", unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Carrera"
        verbose_name_plural = "Carreras"


class Subject(models.Model):
    grade = models.IntegerField(verbose_name="Grado", choices=GRADES_CHOICES)
    name = models.CharField(max_length=255, verbose_name="Nombre")
    tcp2_required = models.BooleanField(verbose_name="Requiere TCP2")
    professor = models.ManyToManyField(Professor, verbose_name="Profesores")

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
    asc = models.FloatField(blank=True, null=True, verbose_name="ACS")
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

    def save(self, *args, **kwargs):
        self.calculate_final_grade()
        return super().save(*args, **kwargs)

    def calculate_final_grade(self):
        if self.tcp1 is None or self.asc is None or self.final_exam is None:
            self.final_grade = 0
            return self.final_grade

        prom_asc = self.asc  # en base a 20
        prom_tcp = self.tcp1 * 0.3  # en base a 30
        if (self.tcp2 is not None) and self.subject.tcp2_required:
            prom_tcp += self.tcp2 * 0.3
            prom_tcp /= 2

        # if self.subject.grade == 9:
        acumulado_base_50 = prom_asc + prom_tcp
        pf_base_50 = self.final_exam / 2
        self.final_grade = acumulado_base_50 + pf_base_50
        # else:
        #     acumulado_base_50 = prom_asc + prom_tcp
        #     self.final_grade = acumulado_base_50 * 2

        return self.final_grade

    def calculate_ranking_score(self):
        if self.tcp1 is None or self.asc is None or self.final_exam is None:
            self.final_grade = 0
            return self.final_grade
        ranking = 0
        prom_asc = self.asc  # en base a 20
        prom_tcp = self.tcp1 * 0.3  # en base a 30
        if (self.tcp2 is not None) and self.subject.tcp2_required:
            prom_tcp += self.tcp2 * 0.3
            prom_tcp /= 2

        if self.subject.grade != 9:
            acumulado_base_50 = prom_asc + prom_tcp
            pf_base_50 = self.final_exam / 2
            ranking = acumulado_base_50 + pf_base_50
        else:
            acumulado_base_50 = prom_asc + prom_tcp
            ranking = acumulado_base_50 * 2

        return ranking

    @staticmethod
    def are_valid(notes):
        if not notes:
            return False
        for note in notes:
            if (
                note.tcp1 is None
                or note.tcp1 < 60
                or note.final_exam is None
                or note.final_exam < 60
                or note.asc is None
                or note.asc < 12
            ):
                return False
            if note.subject.tcp2_required and (
                note.tcp2 is None or note.tcp2 < 60
            ):
                return False

        return True


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

    def __str__(self):
        return f"{self.career.name}-{self.index}"


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

    def __str__(self):
        return f"{self.ranking_number} - {self.ranking_score} - {self.student.first_name} {self.student.last_name}"

    def calculate_ranking_score(self) -> float:
        self.ranking_score = 0
        sume = 0
        notes = StudentNote.objects.filter(student=self.student)
        for note in notes:
            sume += note.calculate_ranking_score()

        if sume == 0 or notes.count() == 0:
            return 0
        self.ranking_score = sume / notes.count()
        return self.ranking_score

    @staticmethod
    def current():
        students = Student.get_students_current_9()
        # approved_students = []
        # for student in students:
        #     if student.their_notes_are_valid():
        #         approved_students.append(student)
        return DegreeScale.objects.filter(student__in=students).order_by(
            "ranking_number"
        )

    @staticmethod
    def calculate_all_ranking_number():
        school_year = SchoolYear.get_current_course()
        students_ranking: List[DegreeScale] = []
        students = Student.get_students_current_9()

        for student in students:
            # if student.ci == "51791253302":
            #     print("estudiante invalido")
            # if student.their_notes_are_valid():
            student_degree_scale: DegreeScale = DegreeScale.objects.filter(
                student=student
            ).first()
            if not student_degree_scale:
                student_degree_scale = DegreeScale.objects.create(
                    student=student, school_year=school_year
                )
            else:
                student_degree_scale.school_year = school_year
            student_degree_scale.calculate_ranking_score()
            student_degree_scale.save()
            students_ranking.append(student_degree_scale)

        students_ranking = sorted(
            students_ranking,
            key=lambda v: v.ranking_score,
            reverse=True,
        )
        for i, ranking in enumerate(students_ranking):
            ranking.ranking_number = i + 1
            ranking.save()

        return students_ranking

    @staticmethod
    def there_are_students_whithout_ranking(course=None):
        if not course:
            course = SchoolYear.get_current_course()
        q = Student.get_students_current_9()
        if q.count() == 0:
            return True
        # count_with_notes_valid = 0
        for student in q:
            # if student.their_notes_are_valid():
            #     count_with_notes_valid += 1
            degree_scale = DegreeScale.objects.filter(
                student=student, school_year=course
            ).first()
            if (
                (not degree_scale)
                or (degree_scale.ranking_score is None)
                or (degree_scale.ranking_number is None)
            ):
                # print(degree_scale)
                # if degree_scale:
                #     print(f"degree_scale.ranking_score {degree_scale.ranking_score}")
                #     print(f"degree_scale.ranking_number {degree_scale.ranking_number}")
                # print(f"ci {student.ci}")
                return True
        return False
        # return count_with_notes_valid == 0


class GrantCareer(models.Model):
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, verbose_name="Estudiante"
    )
    career = models.ForeignKey(
        Career, on_delete=models.CASCADE, verbose_name="Carrera"
    )
    school_year = models.ForeignKey(
        SchoolYear, on_delete=models.CASCADE, verbose_name="Año escolar"
    )

    class Meta:
        verbose_name = "Carrera Otorgada"
        verbose_name_plural = "Carreras Otorgadas"

    def get_ranking(self)->DegreeScale|None:
        return DegreeScale.objects.filter(
            school_year=self.school_year,
            student=self.student
        ).first()

    @staticmethod
    def sort_by_ranking(list_grant_career):
        dict_grant_career_ranking:Dict[GrantCareer,float]={}
        for grant_career in list_grant_career:
            degree_scale=grant_career.get_ranking()
            ranking=degree_scale.ranking_score
            if not ranking:
                ranking=0
            dict_grant_career_ranking[grant_career]=ranking
        response=sorted(dict_grant_career_ranking, key=lambda x: dict_grant_career_ranking[x], )
        return response


    @staticmethod
    def there_are_students_with_no_careers_awarded():
        students = Student.get_students_current_9()
        if students.count() == 0:
            return True
        for student in students:
            if (
                student.their_notes_are_valid()
                and not student.has_career_awarded()
            ):
                return True
        return False

    @staticmethod
    def grant(today=None):
        if today is None:
            today = timezone.now().date()
        careers_amount: Dict[Career, int] = {
            v: v.amount for v in Career.objects.all()
        }
        ranking = DegreeScale.current()
        school_year = SchoolYear.get_current_course()

        grant_career_list: List[GrantCareer] = []
        for rank in ranking:
            student = rank.student
            their_notes_are_valid = student.their_notes_are_valid()
            has_career_awarded = student.has_career_awarded()
            # print(f"their_notes_are_valid {their_notes_are_valid} has_career_awarded {has_career_awarded}")
            if their_notes_are_valid and not has_career_awarded:
                ballot = StudentCareer.objects.filter(student=student).order_by(
                    "index"
                )
                for student_career in ballot:
                    career = student_career.career

                    places_available = careers_amount[career]

                    if places_available:
                        grant_career: GrantCareer = GrantCareer.objects.filter(
                            student=student
                        ).first()
                        if not grant_career:
                            grant_career = GrantCareer.objects.create(
                                student=student,
                                career=career,
                                school_year=school_year,
                            )
                        else:
                            grant_career.career = career
                            grant_career.school_year = school_year
                            grant_career.save()

                        places_available -= 1
                        careers_amount[career] = places_available
                        career.amount = places_available
                        career.save()
                        grant_career_list.append(grant_career)
                        break
        return grant_career_list

    @staticmethod
    def current():
        school_year = SchoolYear.get_current_course()
        return GrantCareer.objects.filter(school_year=school_year)


class SubjectSection(models.Model):
    index = models.IntegerField(verbose_name="Indice", default=1)
    title = models.CharField(max_length=255, verbose_name="Titulo")
    description = models.TextField(
        verbose_name="Descripcion", blank=True, null=True
    )
    subject = models.ForeignKey(
        Subject, on_delete=models.CASCADE, verbose_name="Asignatura"
    )
    school_year = models.ForeignKey(
        SchoolYear, on_delete=models.CASCADE, verbose_name="Año escolar"
    )

    class Meta:
        verbose_name = "Sección de Asignatura"
        verbose_name_plural = "Secciones de Asignaturas"


class Folder(models.Model):
    title = models.CharField(max_length=255, verbose_name="Titulo")
    description = models.TextField(
        verbose_name="Descripcion", blank=True, null=True
    )
    subject_section = models.ForeignKey(
        SubjectSection,
        on_delete=models.CASCADE,
        verbose_name="Sección de Asignatura",
    )

    class Meta:
        verbose_name = "Carpeta"
        verbose_name_plural = "Carpetas"


class File(models.Model):
    title = models.CharField(max_length=255, verbose_name="Titulo")
    description = models.TextField(
        verbose_name="Descripcion", blank=True, null=True
    )
    type = models.CharField(max_length=255, verbose_name="Tipo")
    file = models.CharField(max_length=500, verbose_name="Archivo")

    class Meta:
        abstract = True
        verbose_name = "Archivo"
        verbose_name_plural = "Archivos"


class FileFolder(File):
    folder = models.ForeignKey(
        Folder, on_delete=models.CASCADE, verbose_name="Carpeta"
    )

    class Meta:
        verbose_name = "Archivo De Carpeta"
        verbose_name_plural = "Archivos De Carpetas"


class SchoolTask(models.Model):
    title = models.CharField(max_length=255, verbose_name="Titulo")
    description = models.TextField(
        verbose_name="Descripcion", blank=True, null=True
    )
    date = models.DateField(verbose_name="Fecha")
    # is_acs = models.BooleanField(default=False, verbose_name="Acs")
    # is_tcp = models.BooleanField(default=False, verbose_name="Tcp")
    # is_final_exam = models.BooleanField(
    #     default=False, verbose_name="Examen Final"
    # )
    subject_section = models.ForeignKey(
        SubjectSection,
        on_delete=models.CASCADE,
        verbose_name="Sección de Asignatura",
    )

    class Meta:
        verbose_name = "Tarea Escolar"
        verbose_name_plural = "Tareas Escolares"

    def __str__(self):
        return self.title


class FileSchoolTask(File):
    school_task = models.ForeignKey(
        SchoolTask, on_delete=models.CASCADE, verbose_name="Tarea Escolar"
    )

    class Meta:
        verbose_name = "Archivo De Tarea Escolar"
        verbose_name_plural = "Archivos De Tareas Escolares"


class StudentResponse(models.Model):
    date = models.DateField(verbose_name="Fecha", auto_now=True)
    description = models.TextField(
        verbose_name="Descripcion", blank=True, null=True
    )
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, verbose_name="Estudiante"
    )
    school_task = models.ForeignKey(
        SchoolTask, on_delete=models.CASCADE, verbose_name="Tarea Escolar"
    )

    class Meta:
        verbose_name = "Respuesta del Estudiante"
        verbose_name_plural = "Respuestas de los Estudiantes"

    def __str__(self):
        return f"{self.school_task.title} {self.student.first_name}"


class FileStudentResponse(File):
    student_response = models.ForeignKey(
        StudentResponse,
        on_delete=models.CASCADE,
        verbose_name="Respuesta del Estudiante",
    )

    class Meta:
        verbose_name = "Archivo De Respuesta del Estudiante"
        verbose_name_plural = "Archivos De Respuestas de los Estudiantes"

    def __str__(self):
        return f"{self.title} {self.student_response}"


class SchoolEvent(models.Model):
    date = models.DateTimeField(verbose_name="Fecha")
    title = models.CharField(max_length=255, verbose_name="Titulo")
    description = models.TextField(
        verbose_name="Descripcion", blank=True, null=True
    )

    class Meta:
        verbose_name = "Evento Escolar"
        verbose_name_plural = "Eventos Escolares"
