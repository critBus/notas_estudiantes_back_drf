from django.contrib.auth import get_user_model
from rest_framework.reverse import reverse

from apps.project.models import (
    DegreeScale,
)
from tests.student.parent_case.degree_escale_test_case import (
    DegreeEscaleTestCase,
)

User = get_user_model()


class TestWhithoutRanking(DegreeEscaleTestCase):
    def call_whithout_ranking(
        self,
        unauthorized: bool = False,
        forbidden: bool = False,
        bad_request: bool = False,
        not_found: bool = False,
        print_json_response: bool = False,
    ):
        URL = reverse("degree-scale-exist-whithout")
        response_dict = self.call_get(
            url=URL,
            unauthorized=unauthorized,
            forbidden=forbidden,
            bad_request=bad_request,
            not_found=not_found,
            print_json_response=print_json_response,
        )
        return response_dict

    def validate_whithout_ranking(self, whithout_ranking: bool):
        self.assertEqual(
            whithout_ranking, DegreeScale.there_are_students_whithout_ranking()
        )
        response_dict = self.call_whithout_ranking()
        self.assertDictEqual(
            response_dict, {"are_students_whithout_ranking": whithout_ranking}
        )

    def test_whithout_ranking(self):
        self.validate_whithout_ranking(True)
        students = [self.create_random_student(grade=9) for _ in range(10)]
        self.validate_whithout_ranking(True)
        for student in students[1:]:
            self.ponerle_notas_validas_al_estudiante(student=student)
        self.validate_whithout_ranking(True)
        DegreeScale.calculate_all_ranking_number()
        self.validate_whithout_ranking(False)
        self.ponerle_notas_validas_al_estudiante(student=students[0])
        self.validate_whithout_ranking(True)
        DegreeScale.calculate_all_ranking_number()
        self.validate_whithout_ranking(False)
