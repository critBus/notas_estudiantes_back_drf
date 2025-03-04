from typing import List

from apps.project.models import DegreeScale, Student
from apps.project.utils.util_reporte_d import custom_export_report_by_name


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


generar_reporte_certificacion_notas_pdf.short_description = (
    "Generar Reporte Escalafón"
)
