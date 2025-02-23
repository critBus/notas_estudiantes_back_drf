from django.contrib.auth import get_user_model
from rest_framework.reverse import reverse

from apps.project.models import (
    DegreeScale,
    SchoolYear,
    StudentNote,
    Subject,
)
from tests.student.parent_case.degree_escale_test_case import (
    DegreeEscaleTestCase,
)

User = get_user_model()


class TestDegreeEscale(DegreeEscaleTestCase):
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
        self.assertEqual(int(ranking), int(degree_scale.ranking_score))

    def test_degree_escale(self):
        self.create_fake_ranking()
        DegreeScale.calculate_all_ranking_number()
        q = DegreeScale.objects.order_by("ranking_number")
        self.assertEqual(3, q.count())
        for i, degree in enumerate(q):
            self.assertEqual(i + 1, degree.ranking_number)

    def call_degree_scale_calculated(
        self,
        unauthorized: bool = False,
        forbidden: bool = False,
        bad_request: bool = False,
        not_found: bool = False,
        print_json_response: bool = False,
    ):
        URL = reverse("degree-scale-calculated")
        response_dict = self.call_get(
            url=URL,
            unauthorized=unauthorized,
            forbidden=forbidden,
            bad_request=bad_request,
            not_found=not_found,
            print_json_response=print_json_response,
        )

        return response_dict

    def call_degree_scale_current(
        self,
        unauthorized: bool = False,
        forbidden: bool = False,
        bad_request: bool = False,
        not_found: bool = False,
        print_json_response: bool = False,
    ):
        URL = reverse("degree-scale-current")
        response_dict = self.call_get(
            url=URL,
            unauthorized=unauthorized,
            forbidden=forbidden,
            bad_request=bad_request,
            not_found=not_found,
            print_json_response=print_json_response,
        )

        return response_dict

    def test_degree_scale_calculated(self):
        students = self.create_fake_ranking()
        response_dict = self.call_degree_scale_calculated(
            print_json_response=False
        )
        rankings = []
        for student in students:
            ranking = DegreeScale.objects.filter(student=student).first()
            self.assertIsNotNone(ranking)
            rankings.append(ranking)
        self.assertEqual(
            response_dict,
            [
                {
                    "id": rank.id,
                    "student": {
                        "id": rank.student.id,
                        "is_approved": True,
                        "ci": rank.student.ci,
                        "address": rank.student.address,
                        "grade": 9,
                        "last_name": rank.student.last_name,
                        "first_name": rank.student.first_name,
                        "registration_number": rank.student.registration_number,
                        "sex": rank.student.sex,
                        "is_graduated": False,
                        "is_dropped_out": False,
                        "user": None,
                    },
                    "school_year": {
                        "id": rank.school_year.id,
                        "start_date": str(rank.school_year.start_date),
                        "end_date": str(rank.school_year.end_date),
                        "name": rank.school_year.name,
                    },
                    "ranking_score": rank.ranking_score,
                    "ranking_number": i + 1,
                }
                for i, rank in enumerate(rankings)
            ],
        )

    def test_degree_scale_current(self):
        students = self.create_fake_ranking()
        DegreeScale.calculate_all_ranking_number()
        response_dict = self.call_degree_scale_current(
            print_json_response=False
        )
        rankings = []
        for student in students:
            ranking = DegreeScale.objects.filter(student=student).first()
            self.assertIsNotNone(ranking)
            rankings.append(ranking)
        self.assertEqual(
            response_dict,
            [
                {
                    "id": rank.id,
                    "student": {
                        "id": rank.student.id,
                        "is_approved": True,
                        "ci": rank.student.ci,
                        "address": rank.student.address,
                        "grade": 9,
                        "last_name": rank.student.last_name,
                        "first_name": rank.student.first_name,
                        "registration_number": rank.student.registration_number,
                        "sex": rank.student.sex,
                        "is_graduated": False,
                        "is_dropped_out": False,
                        "user": None,
                    },
                    "school_year": {
                        "id": rank.school_year.id,
                        "start_date": str(rank.school_year.start_date),
                        "end_date": str(rank.school_year.end_date),
                        "name": rank.school_year.name,
                    },
                    "ranking_score": rank.ranking_score,
                    "ranking_number": i + 1,
                }
                for i, rank in enumerate(rankings)
            ],
        )
