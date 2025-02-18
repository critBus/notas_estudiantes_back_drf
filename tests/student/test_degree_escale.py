from django.contrib.auth import get_user_model

from apps.project.models import (
    DegreeScale,
    SchoolYear,
    StudentNote,
    Subject,
)
from tests.student.parent_case.student_test_case import StudentTestCase

User = get_user_model()


class TestDegreeEscale(StudentTestCase):
    def test_calculate_final_grade(self):
        student = self.create_random_student(grade=9)
        curso = SchoolYear.get_current_course()
        subject = Subject.objects.create(
            grade=9, name="test", tcp2_required=True
        )
        nota = StudentNote.objects.create(
            subject=subject, student=student, school_year=curso
        )
        nota.tcp1 = 70
        nota.tcp2 = 80
        nota.asc = 8
        nota.final_exam = 65

        final_grade = 8 + ((70 * 0.4) + (80 * 0.4)) / 2 + 65 / 2
        # print(f"final_grade {final_grade}")
        nota.calculate_final_grade()
        self.assertEqual(nota.final_grade, final_grade)

        subject.tcp2_required = False
        subject.save()
        final_grade = 8 + 70 * 0.4 + 65 / 2
        nota.calculate_final_grade()
        self.assertEqual(nota.final_grade, final_grade)

        subject.grade = 8
        subject.save()
        student.grade = 8
        student.save()
        final_grade = (8 + 70 * 0.4) * 2
        nota.calculate_final_grade()
        self.assertEqual(nota.final_grade, final_grade)

        subject.tcp2_required = True
        subject.save()
        final_grade = (8 + ((70 * 0.4) + (80 * 0.4)) / 2) * 2
        nota.calculate_final_grade()
        self.assertEqual(nota.final_grade, final_grade)

    def test_calculate_ranking_score(self):
        student = self.create_random_student(grade=9)
        curse_7, curse_8, curse_9 = self.create_3_school_year(2022)

        subject_7 = Subject.objects.create(
            grade=7, name="test_7", tcp2_required=True
        )
        subject_8 = Subject.objects.create(
            grade=8, name="test_8", tcp2_required=True
        )
        subject_9 = Subject.objects.create(
            grade=9, name="test_9", tcp2_required=True
        )

        note_7 = StudentNote.objects.create(
            subject=subject_7, student=student, school_year=curse_7
        )
        note_7.tcp1 = 70
        note_7.tcp2 = 80
        note_7.asc = 8
        note_7.final_exam = 65
        note_7.save()
        final_grade_7 = (8 + ((70 * 0.4) + (80 * 0.4)) / 2) * 2

        note_8 = StudentNote.objects.create(
            subject=subject_8, student=student, school_year=curse_8
        )
        note_8.tcp1 = 81
        note_8.tcp2 = 62
        note_8.asc = 7
        note_8.final_exam = 78
        note_8.save()
        final_grade_8 = (7 + ((81 * 0.4) + (62 * 0.4)) / 2) * 2

        note_9 = StudentNote.objects.create(
            subject=subject_9, student=student, school_year=curse_9
        )
        note_9.tcp1 = 98
        note_9.tcp2 = 79
        note_9.asc = 9
        note_9.final_exam = 96
        note_9.save()
        final_grade_9 = 9 + ((98 * 0.4) + (79 * 0.4)) / 2 + 96 / 2

        ranking = (final_grade_7 + final_grade_8 + final_grade_9) / 3
        # print(f"ranking {ranking}")

        degree_scale = DegreeScale.objects.create(
            student=student,
            school_year=curse_9,
        )
        degree_scale.calculate_ranking_score()
        self.assertEqual(ranking, degree_scale.ranking_score)

    def test_degree_escale(self):
        SchoolYear.objects.all().delete()
        Subject.objects.all().delete()
        curse_7, curse_8, curse_9 = self.create_3_school_year(2022)
        for i in range(3):
            grade = i + 7
            Subject.objects.create(
                grade=grade, name=f"test_{grade}", tcp2_required=True
            )

        for i in range(3):
            student = self.create_random_student(grade=9)
            for j in range(3):
                grade = j + 7
                note = StudentNote.objects.create(
                    subject=Subject.objects.get(name=f"test_{grade}"),
                    student=student,
                    school_year=SchoolYear.objects.get(
                        start_date__year=2022 + j
                    ),
                )
                note.tcp1 = 90 + i + j
                note.tcp2 = 79 + i + j
                note.asc = 6 + i + j
                note.final_exam = 92 + i + j
                note.save()

        DegreeScale.calculate_all_ranking_number()
        q = DegreeScale.objects.order_by("ranking_number")
        self.assertEqual(3, q.count())
        for i, degree in enumerate(q):
            self.assertEqual(i + 1, degree.ranking_number)
