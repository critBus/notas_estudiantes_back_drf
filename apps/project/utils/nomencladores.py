from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django_reportbroD.models import ReportDefinition, ReportRequest

from apps.project.models import (
    ROL_NAME_ADMIN,
    ROL_NAME_PROFESSOR,
    ROL_NAME_SECRETARY,
    ROL_NAME_STUDENT,
    ApprovedSchoolCourse,
    Career,
    DegreeScale,
    Dropout,
    FileFolder,
    FileSchoolTask,
    FileStudentResponse,
    Folder,
    GrantCareer,
    Professor,
    SchoolEvent,
    SchoolTask,
    SchoolYear,
    Student,
    StudentCareer,
    StudentNote,
    StudentResponse,
    Subject,
    SubjectSection,
)
from config.utils.utils_permission import crear_rol

User = get_user_model()


def crear_roles_django_default():
    crear_rol(
        lista_modelos=[
            SchoolYear,
            Student,
            ApprovedSchoolCourse,
            Dropout,
            Career,
            Professor,
            Subject,
            StudentNote,
            StudentCareer,
            DegreeScale,
            GrantCareer,
            SubjectSection,
            Folder,
            FileFolder,
            SchoolTask,
            FileSchoolTask,
            StudentResponse,
            FileStudentResponse,
            SchoolEvent,
            ReportRequest,
            ReportDefinition,
            User,
            Group,
            Permission,
        ],
        lista_modelos_solo_update=[],
        lista_modelos_solo_create=[],
        lista_modelos_solo_view=[],
        nombre_rol=ROL_NAME_ADMIN,
    )
    crear_rol(
        nombre_rol=ROL_NAME_STUDENT,
    )
    crear_rol(
        nombre_rol=ROL_NAME_PROFESSOR,
    )
    crear_rol(
        nombre_rol=ROL_NAME_SECRETARY,
    )
