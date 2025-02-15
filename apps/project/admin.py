# Register your models here.
from django.contrib import admin

from apps.project.models import (
    Career,
    DegreeScale,
    SchoolYear,
    Student,
    StudentCareer,
    StudentNote,
    Subject,
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
