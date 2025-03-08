# Register your models here.
from django.contrib import admin

from apps.project.models import (
    ApprovedSchoolCourse,
    Career,
    DegreeScale,
    Dropout,
    FileStudentResponse,
    GrantCareer,
    Professor,
    SchoolYear,
    Student,
    StudentCareer,
    StudentGroup,
    StudentNote,
    StudentResponse,
    Subject,
    SubjectSection,
)


@admin.register(SchoolYear)
class SchoolYearAdmin(admin.ModelAdmin):
    list_display = (
        "start_date",
        "end_date",
        "name",
    )
    list_filter = (
        "start_date",
        "end_date",
    )
    search_fields = ("name",)
    date_hierarchy = "start_date"
    ordering = list(list_display).copy()
    list_display_links = list(list_display).copy()


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "ci",
        "grade",
        "last_name",
        "first_name",
        "registration_number",
        "sex",
        "is_graduated",
        "is_dropped_out",
    )
    list_filter = (
        "grade",
        "sex",
        "is_graduated",
        "is_dropped_out",
    )
    search_fields = (
        "id",
        "ci",
        "grade",
        "last_name",
        "first_name",
        "registration_number",
        "sex",
        "is_graduated",
        "is_dropped_out",
    )
    ordering = list(list_display).copy()
    list_display_links = list(list_display).copy()


@admin.register(Career)
class CareerAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
    ordering = list(list_display).copy()
    list_display_links = list(list_display).copy()


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "grade",
        "tcp2_required",
    )
    list_filter = (
        "grade",
        "tcp2_required",
    )
    search_fields = ("name",)
    filter_horizontal = ("professor",)
    ordering = list(list_display).copy()
    list_display_links = list(list_display).copy()


@admin.register(StudentNote)
class StudentNoteAdmin(admin.ModelAdmin):
    list_display = (
        "student",
        "subject",
        "asc",
        "final_grade",
        "final_exam",
        "tcp1",
        "tcp2",
        "school_year",
    )
    list_filter = (
        "student",
        "subject",
        "asc",
        "final_grade",
        "final_exam",
        "tcp1",
        "tcp2",
        "school_year",
    )
    ordering = list(list_display).copy()
    list_display_links = list(list_display).copy()


@admin.register(StudentCareer)
class StudentCareerAdmin(admin.ModelAdmin):
    list_display = (
        "career",
        "student",
        "index",
    )
    list_filter = (
        "career",
        "student",
        "index",
    )
    ordering = list(list_display).copy()
    list_display_links = list(list_display).copy()


@admin.register(DegreeScale)
class DegreeScaleAdmin(admin.ModelAdmin):
    list_display = ("student", "school_year", "ranking_score", "ranking_number")
    list_filter = ("student", "school_year", "ranking_score", "ranking_number")
    ordering = list(list_display).copy()
    list_display_links = list(list_display).copy()


@admin.register(GrantCareer)
class GrantCareerAdmin(admin.ModelAdmin):
    list_display = (
        "student",
        "career",
        "approved_school_course",
    )
    list_filter = (
        "career",
        "approved_school_course",
    )
    ordering = list(list_display).copy()
    list_display_links = list(list_display).copy()


@admin.register(Dropout)
class DropoutAdmin(admin.ModelAdmin):
    list_display = (
        "date",
        "municipality",
        "province",
        "school",
        "student",
        "is_dropout",
    )
    list_filter = ("date", "municipality", "province", "school", "is_dropout")
    search_fields = (
        "municipality",
        "province",
        "school",
    )
    date_hierarchy = "date"
    ordering = list(list_display).copy()
    list_display_links = list(list_display).copy()


@admin.register(ApprovedSchoolCourse)
class ApprovedSchoolCourseAdmin(admin.ModelAdmin):
    list_display = ("date", "student", "grade", "school_year")
    list_filter = ("date", "student", "grade", "school_year")
    date_hierarchy = "date"
    ordering = list(list_display).copy()
    list_display_links = list(list_display).copy()


@admin.register(Professor)
class ProfessorAdmin(admin.ModelAdmin):
    list_display = (
        "ci",
        "last_name",
        "first_name",
        "sex",
    )
    list_filter = ("sex",)
    search_fields = (
        "ci",
        "grade",
        "last_name",
        "first_name",
        "registration_number",
        "sex",
    )
    ordering = list(list_display).copy()
    list_display_links = list(list_display).copy()


@admin.register(StudentResponse)
class StudentResponseAdmin(admin.ModelAdmin):
    list_display = (
        "date",
        "student",
        "school_task",
    )
    list_filter = ("date", "student", "school_task")
    date_hierarchy = "date"
    ordering = list(list_display).copy()
    list_display_links = list(list_display).copy()


@admin.register(FileStudentResponse)
class FileStudentResponseeAdmin(admin.ModelAdmin):
    list_display = (
        "student_response",
        "title",
        "description",
        "type",
    )
    list_filter = (
        "student_response",
        "type",
    )
    search_fields = ("title",)
    ordering = list(list_display).copy()
    list_display_links = list(list_display).copy()


@admin.register(StudentGroup)
class StudentGroupResponseeAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "grade",
    )
    list_filter = ("grade",)
    search_fields = ("name",)
    filter_horizontal = ("professors",)
    ordering = list(list_display).copy()
    list_display_links = list(list_display).copy()


@admin.register(SubjectSection)
class SubjectSectionAdmin(admin.ModelAdmin):
    list_display = (
        "index",
        "title",
        "subject",
        "school_year",
    )
    list_filter = ("index", "school_year", "subject")
    ordering = list(list_display).copy()
    list_display_links = list(list_display).copy()
