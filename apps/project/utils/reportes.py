from typing import List

from apps.project.models import DegreeScale, Student, StudentNote
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


generar_reporte_escalafon_pdf.short_description = "Generar Reporte Escalafón"


def generar_reporte_certificacion_notas_pdf(student: Student, queryset):
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
        "grade": student.grade,
        "nombre_completo": f"{student.first_name} {student.last_name if student.last_name else ''}".strip(),
    }
    return custom_export_report_by_name(
        "Certificacion De Notas", data, file="Escalafon"
    )


generar_reporte_certificacion_notas_pdf.short_description = (
    "Generar Reporte Escalafón"
)
