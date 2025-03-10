from typing import List

from apps.project.models import (
    DegreeScale,
    Dropout,
    Student,
    StudentNote,
    Subject,
)
from apps.project.utils.util_reporte_d import custom_export_report_by_name


def format_float(value):
    if value is None:
        return "-"
    else:
        return f"{value:.2f}"


def generar_reporte_escalafon_pdf(queryset):
    entidades: List[DegreeScale] = queryset
    lista = []
    for entidad in entidades:
        data_entidad = {
            "first_name": entidad.student.first_name,
            "last_name": entidad.student.last_name,
            "ci": entidad.student.ci,
            "ranking_score": entidad.ranking_score,
            "ranking_number": entidad.ranking_number,
        }
        lista.append(data_entidad)

    data = {
        "lista": lista,
    }
    return custom_export_report_by_name("Escalafon", data, file="Escalafon")


def generar_reporte_certificacion_notas_pdf(
    student: Student, queryset, grade: int
):
    entidades: List[StudentNote] = queryset
    lista = []
    for entidad in entidades:
        data_entidad = {
            "name": entidad.subject.name,
            "asc": format_float(entidad.asc),
            "tcp1": format_float(entidad.tcp1),
            "tcp2": format_float(entidad.tcp2),
            "final_exam": format_float(entidad.final_exam),
            "final_grade": format_float(entidad.final_grade),
        }
        lista.append(data_entidad)

    data = {
        "lista": lista,
        "ci": student.ci,
        "grade": grade,
        "nombre_completo": f"{student.first_name} {student.last_name if student.last_name else ''}".strip(),
    }
    return custom_export_report_by_name(
        "Certificacion De Notas", data, file="Certificacion De Notas"
    )


def generar_reporte_notas_de_asignatura_pdf(subject: Subject, queryset):
    entidades: List[StudentNote] = queryset
    lista = []
    for entidad in entidades:
        data_entidad = {
            "ci": entidad.student.ci,
            "nombre_completo": f"{entidad.student.first_name} {entidad.student.last_name if entidad.student.last_name else ''}".strip(),
            "asc": format_float(entidad.asc),
            "tcp1": format_float(entidad.tcp1),
            "tcp2": format_float(entidad.tcp2),
            "final_exam": format_float(entidad.final_exam),
            "final_grade": format_float(entidad.final_grade),
        }
        lista.append(data_entidad)

    data = {
        "lista": lista,
        "grade": subject.grade,
        "name": subject.name,
    }
    return custom_export_report_by_name(
        "Notas De Asignatura", data, file="Notas De Asignatura"
    )


def generar_reporte_estudiantes_pdf(queryset):
    entidades: List[Student] = queryset
    lista = []
    for entidad in entidades:
        data_entidad = {
            "first_name": entidad.first_name,
            "last_name": entidad.last_name if entidad.last_name else "-",
            "ci": entidad.ci,
            "grade": str(entidad.grade),
            "registration_number": str(entidad.registration_number),
            "sex": entidad.sex,
            "is_graduated": "Si" if entidad.is_graduated else "No",
            "is_dropped_out": "Si" if entidad.is_dropped_out else "No",
            "address": entidad.address if entidad.address else "-",
            "group": "-",
        }
        lista.append(data_entidad)

    data = {
        "lista": lista,
    }
    return custom_export_report_by_name("Estudiantes", data, file="Estudiantes")


def generar_reporte_bajas_pdf(queryset):
    entidades: List[Dropout] = queryset
    lista = []
    for entidad in entidades:
        data_entidad = {
            "first_name": entidad.student.first_name,
            "last_name": entidad.student.last_name
            if entidad.student.last_name
            else "-",
            "ci": entidad.student.ci,
            "grade": str(entidad.student.grade),
            "registration_number": str(entidad.student.registration_number),
            "sex": entidad.student.sex,
            "is_graduated": "Si" if entidad.student.is_graduated else "No",
            "is_dropped_out": "Si" if entidad.student.is_dropped_out else "No",
            "address": entidad.student.address
            if entidad.student.address
            else "-",
            "group": "-",
            "municipality": entidad.municipality,
            "province": entidad.province,
            "school": entidad.school,
            "year_mount": f"{entidad.date.year}-{entidad.date.month}",
            "year": str(entidad.date.year),
            "mes": str(entidad.date.month),
            "is_dropout": "Si" if entidad.is_dropout else "No",
        }
        lista.append(data_entidad)

    data = {
        "lista": lista,
    }
    return custom_export_report_by_name("Altas Bajas", data, file="Altas Bajas")
