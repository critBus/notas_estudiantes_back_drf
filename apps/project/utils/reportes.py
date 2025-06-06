from typing import List, Dict

from django.utils import timezone
from collections import defaultdict

from apps.project.models import (
    DegreeScale,
    Dropout,
    Student,
    StudentNote,
    Subject,
    SchoolYear,
    GrantCareer,
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

    current_year = SchoolYear.get_current_course()

    data = {"lista": lista, "fecha": timezone.now().date(), "school_year":current_year.name if current_year else "No disponible"}
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
            "tcp2": format_float(entidad.tcp2)
            if entidad.subject.tcp2_required
            else "-",
            "final_exam": format_float(entidad.final_exam),
            "final_grade": format_float(entidad.final_grade),
        }
        lista.append(data_entidad)

    data = {
        "lista": lista,
        "ci": student.ci,
        "grade": grade,
        "nombre_completo": f"{student.first_name} {student.last_name if student.last_name else ''}".strip(),
        "fecha": timezone.now().date(),
    }
    return custom_export_report_by_name(
        "Certificacion De Notas", data, file="Certificacion De Notas"
    )


def generar_reporte_certificacion_notas_todas_pdf(student: Student):
    entidades: List[StudentNote] = StudentNote.objects.filter(
        student=student
    ).order_by("subject__grade", "subject")
    lista = []
    for entidad in entidades:
        data_entidad = {
            "name": entidad.subject.name,
            "asc": format_float(entidad.asc),
            "tcp1": format_float(entidad.tcp1),
            "tcp2": format_float(entidad.tcp2)
            if entidad.subject.tcp2_required
            else "-",
            "final_exam": format_float(entidad.final_exam),
            "final_grade": format_float(entidad.final_grade),
            "grade": str(entidad.subject.grade),
        }
        lista.append(data_entidad)

    data = {
        "lista": lista,
        "ci": student.ci,
        "nombre_completo": f"{student.first_name} {student.last_name if student.last_name else ''}".strip(),
        "fecha": timezone.now().date(),
    }
    return custom_export_report_by_name(
        "Certificacion De Notas Por Estudiante",
        data,
        file="Certificacion De Notas Por Estudiante",
    )


def generar_reporte_notas_de_asignatura_pdf(subject: Subject, queryset):
    entidades: List[StudentNote] = queryset.order_by("student__group__name", "student__first_name", "student__last_name")
    lista = []
    for entidad in entidades:
        data_entidad = {
            "ci": entidad.student.ci,
            "nombre_completo": f"{entidad.student.first_name} {entidad.student.last_name if entidad.student.last_name else ''}".strip(),
            "asc": format_float(entidad.asc),
            "tcp1": format_float(entidad.tcp1),
            "tcp2": format_float(entidad.tcp2)
            if entidad.subject.tcp2_required
            else "-",
            "final_exam": format_float(entidad.final_exam),
            "final_grade": format_float(entidad.final_grade),
            "group": entidad.student.group.name if entidad.student.group else "-",
        }
        lista.append(data_entidad)

    data = {
        "lista": lista,
        "grade": subject.grade,
        "name": subject.name,
        "fecha": timezone.now().date(),
    }
    return custom_export_report_by_name(
        "Notas De Asignatura", data, file="Notas De Asignatura"
    )


def generar_reporte_estudiantes_pdf(queryset):
    entidades: List[Student] = queryset.order_by("grade", "group__name")
    lista = []

    for entidad in entidades:
        sufijos = {7: "mo", 8: "vo", 9: "no"}
        grado = entidad.grade
        grado_formateado = f"{grado}{sufijos.get(grado, '')}"
        data_entidad = {
            "first_name": entidad.first_name,
            "last_name": entidad.last_name if entidad.last_name else "-",
            "ci": entidad.ci,
            "grade": grado_formateado,
            "registration_number": str(entidad.registration_number),
            "sex": entidad.sex,
            "is_graduated": "Si" if entidad.is_graduated else "No",
            "is_dropped_out": "Si" if entidad.is_dropped_out else "No",
            "address": entidad.address if entidad.address else "-",
            "group": entidad.group.name if entidad.group else "-",
        }
        lista.append(data_entidad)

    current_year = SchoolYear.get_current_course()

    data = {
        "lista": lista,
        "fecha": timezone.now().date(),
        "school_year":current_year.name if current_year else "No disponible"
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

    data = {"lista": lista, "fecha": timezone.now().date()}
    return custom_export_report_by_name("Altas Bajas", data, file="Altas Bajas")

def generar_reporte_carreras_otorgadas_pdf():
    escalafon: List[DegreeScale] = DegreeScale.current()
    lista = []

    for escala in escalafon:
        student = escala.student
        grant = GrantCareer.objects.filter(student=student).first()
        if grant:
            data_entidad = {
                "ranking_number": escala.ranking_number,
                "ranking_score": escala.ranking_score,
                "first_name": student.first_name,
                "last_name": student.last_name or "-",
                "ci": student.ci,
                "career": grant.career.name,
            }
            lista.append(data_entidad)

    current_year = DegreeScale.current().first().school_year if escalafon else None

    data = {
        "lista": lista,
        "fecha": timezone.now().date(),
        "school_year": current_year.name if current_year else "No disponible"
    }

    return custom_export_report_by_name("Otorgamiento", data, file="Carreras_Otorgadas")

def generar_reporte_certificacion_notasFinales_pdf(
    student: Student, queryset, grade: int
):
    entidades: List[StudentNote] = queryset
    lista = []
    promedio = 0
    suma = 0
    cantidad = 0
    for entidad in entidades:
        data_entidad = {
            "name": entidad.subject.name,
            "final_grade": format_float(entidad.final_grade),
        }
        suma += entidad.final_grade
        cantidad += 1
        lista.append(data_entidad)
    promedio = suma / cantidad if cantidad > 0 else 0
    data = {
        "promedio": promedio,
        "lista": lista,
        "ci": student.ci,
        "grade": grade,
        "nombre_completo": f"{student.first_name} {student.last_name if student.last_name else ''}".strip(),
        "fecha": timezone.now().date(),
    }
    return custom_export_report_by_name(
        "Certificacion De NotasFinales", data, file="Certificacion De NotasFinales"
    )

def generar_reporte_certificacion_notasFinales_todas_pdf(student: Student):
    entidades: List[StudentNote] = StudentNote.objects.filter(
        student=student
    ).order_by("subject__grade", "subject")

    lista = []
    promedios_por_grado = defaultdict(list)

    for entidad in entidades:
        grado = entidad.subject.grade
        if entidad.final_grade is not None:
            promedios_por_grado[grado].append(entidad.final_grade)

        data_entidad = {
            "name": entidad.subject.name,
            "final_grade": format_float(entidad.final_grade),
            "grade": str(grado),
        }
        lista.append(data_entidad)

    # Calcular el promedio por grado
    promedios = []
    for grado, notas in promedios_por_grado.items():
        promedio = sum(notas) / len(notas) if notas else 0
        promedios.append({
            "grade": str(grado),
            "promedio": format_float(promedio)
        })

    data = {
        "lista": lista,
        "promedios": promedios,  # Lista de promedios por grado
        "ci": student.ci,
        "nombre_completo": f"{student.first_name} {student.last_name or ''}".strip(),
        "fecha": timezone.now().date(),
    }

    return custom_export_report_by_name(
        "Certificacion De NotasFinales Por Estudiante",
        data,
        file="Certificacion De NotasFinales Por Estudiante",
    )
