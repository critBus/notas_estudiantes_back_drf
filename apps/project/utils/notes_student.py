from apps.project.models import SchoolYear,StudentNote,Student
from datetime import timedelta
from collections import defaultdict
from typing import Dict,List
def get_student_school_year_grades(student:Student)->Dict[SchoolYear,int]:
    # Obtener todos los años escolares ordenados por fecha de inicio
    all_school_years = list(SchoolYear.objects.order_by("start_date"))
    
    if not all_school_years:
        raise ValueError("No hay años escolares definidos.")

    current_year = SchoolYear.get_current_course()
    if not current_year:
        current_year = all_school_years[-1]  # Último año como fallback

    current_grade = student.grade
    if current_grade not in [7, 8, 9]:
        raise ValueError("El estudiante no está en un grado válido (7, 8 o 9).")

    grades_to_check = list(range(current_grade, 6, -1))  # Ej: [9, 8, 7]
    school_year_grades = {}

    # Buscar el índice del último año conocido (inicialmente es el año actual)
    try:
        last_known_index = all_school_years.index(current_year)
    except ValueError:
        last_known_index = len(all_school_years) - 1  # Si no está, usar el más reciente

    for grade in grades_to_check:
        # Buscar si hay notas para este grado
        notes_for_grade = StudentNote.objects.filter(
            student=student,
            subject__grade=grade
        ).select_related('school_year', 'subject')

        if notes_for_grade.exists():
            for note in notes_for_grade:
                school_year_grades[note.school_year] = grade
            # Actualizar el último año conocido al más reciente de este grado
            latest_note_year = notes_for_grade.order_by('-school_year__start_date').first().school_year
            try:
                last_known_index = all_school_years.index(latest_note_year)
            except ValueError:
                pass  # No debería ocurrir si ya existe en la base de datos
        else:
            # No hay notas, intentar inferir el año anterior
            if last_known_index > 0:
                last_known_index -= 1
                inferred_year = all_school_years[last_known_index]
                school_year_grades[inferred_year] = grade
            else:
                print(f"⚠️ No se puede inferir un año escolar anterior para el grado {grade}.")
                break

    return school_year_grades


# def get_student_school_year_grades2(student):
#     # Obtener todos los años escolares ordenados por fecha de inicio
#     all_school_years = list(SchoolYear.objects.order_by("start_date"))

#     current_year = SchoolYear.get_current_course()
#     if not current_year:
#         raise ValueError("No hay un año escolar actual definido.")

#     current_grade = student.grade
#     if current_grade not in [7, 8, 9]:
#         raise ValueError("El estudiante no está en un grado válido (7, 8 o 9).")

#     # Generar la secuencia de grados: desde el actual hasta 7
#     grades_to_check = list(range(current_grade, 6, -1))  # Ej: [9, 8, 7]

#     school_year_grades = {}
#     last_known_year = current_year  # Asumimos que el año actual es el más reciente

#     for grade in grades_to_check:
#         # Buscar notas del estudiante para este grado
#         notes_for_grade = StudentNote.objects.filter(
#             student=student,
#             subject__grade=grade
#         ).select_related('school_year', 'subject')

#         if notes_for_grade.exists():
#             # Usamos todos los años escolares asociados a este grado
#             for note in notes_for_grade:
#                 school_year_grades[note.school_year] = grade
#             # Actualizamos el último año conocido
#             last_known_year = notes_for_grade.order_by('-school_year__start_date').first().school_year
#         else:
#             # No hay notas para este grado, inferimos el año
#             if last_known_year:
#                 # Calculamos el año anterior (aproximadamente 1 año antes)
#                 inferred_start_date = last_known_year.start_date - timedelta(days=365)
#                 inferred_end_date = last_known_year.end_date - timedelta(days=365)

#                 # Buscamos un SchoolYear que coincida con estas fechas aproximadas
#                 inferred_year = SchoolYear.objects.filter(
#                     start_date__year=inferred_start_date.year
#                 ).order_by('start_date').first()

#                 if inferred_year:
#                     school_year_grades[inferred_year] = grade
#                     last_known_year = inferred_year
#                 else:
#                     print(f"⚠️ No se encontró un año escolar para el grado {grade} (año inferido: {inferred_start_date.year}-{inferred_start_date.year + 1})")
#                     last_known_year = None
#             else:
#                 print(f"⚠️ No se puede inferir el año escolar para el grado {grade}, no hay un año conocido previo.")
#                 break

#     return school_year_grades