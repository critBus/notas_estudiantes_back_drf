from typing import Any, Dict

from rest_framework.reverse import reverse  # Para generar urls

from tests.utils.mixin.api_crud_mixin import ApiCrudMixin


class SubjectSectionMixin(ApiCrudMixin):
    def call_create_subject_section(
        self,
        id: int,
        payload: Dict[str, Any],
        unauthorized: bool = False,
        forbidden: bool = False,
        bad_request: bool = False,
        not_found: bool = False,
        print_json_response: bool = False,
    ):
        URL = reverse("subject-section-create", args=[id])
        response_dict = self.call_post(
            payload=payload,
            url=URL,
            unauthorized=unauthorized,
            forbidden=forbidden,
            bad_request=bad_request,
            not_found=not_found,
            print_json_response=print_json_response,
            format_json=True,
        )

        return response_dict
