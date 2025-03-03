import json
import os

from django.conf import settings
from django.http import HttpResponse, HttpResponseServerError
from django.utils import timezone
from django_reportbroD.models import ReportDefinition
from reportbro import Report, ReportBroError


def custom_export_report_by_name(template_name, data, file="reporte"):
    """Export a report using its name"""

    report = ReportDefinition.objects.filter(name=template_name).first()

    if not report:
        return HttpResponseServerError(
            "Este reporte no se encuentra disponible"
        )

    # if extension.lower() == "xlsx":
    #     return reportXLSX(report.report_definition, data, file)

    return customReportPDF(report.report_definition, data, file, template_name)


def customReportPDF(
    report_definition, data, file="reporte", nombre_reporte=None
):
    """Prints a pdf file with the available data and optionally sends it as an email attachment."""

    try:
        report_inst = Report(json.loads(report_definition), data)

        if report_inst.errors:
            raise ReportBroError(report_inst.errors[0])

        pdf_report = report_inst.generate_pdf()

        response = HttpResponse(
            bytes(pdf_report), content_type="application/pdf"
        )
        response["Content-Disposition"] = (
            'attachment; filename="{filename}"'.format(filename=f"{file}.pdf")
        )

        return response
    except Exception as e:
        # Handle any exceptions or errors that may occur during the process
        print(f"An error occurred: {str(e)}")
        return HttpResponse("An error occurred while processing the report")


def load_json(filename):
    actual = timezone.now()
    file = json.load(open(filename, "r"))
    name = file["name"]
    namereport = (
        name
        if ReportDefinition.objects.filter(name=name).first() is None
        else name + " " + actual.isoformat()
    )
    ReportDefinition.objects.create(
        name=namereport,
        report_definition=file["report_definition"],
        remark=file["remark"],
        last_modified_at=actual,
    )
    print(f"reporte cargado: {name}")


def load_automatic_reports(folder="reportes"):
    print("cargando reportes ...")
    dire = os.path.join(settings.BASE_DIR, folder)
    for filename in os.listdir(dire):
        load_json(os.path.join(dire, filename))
