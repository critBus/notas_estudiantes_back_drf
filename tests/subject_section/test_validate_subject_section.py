
from django.contrib.auth import get_user_model

from apps.project.models import (
    Subject,
)
from tests.subject_section.parent_case.subject_section_test_case import (
    SubjectSectionTestCase,
)

User = get_user_model()


class TestValidateCreateSubjectSection(SubjectSectionTestCase):
    def test_validate_subject_section(self):
        subject = Subject.objects.first()
        data = [
            {
                "index": 2147483647,
                "title": "secciontest",
                "description": "string",
                "folders": [
                    {
                        "title": "string",
                        "description": "string",
                        "files": [
                            {
                                "title": "string",
                                "description": "string",
                                "file": "string",
                            }
                        ],
                    },
                    {
                        "title": "string",
                        "description": "string",
                        "files": [
                            {
                                "title": "string",
                                "description": "string",
                                "file": "string",
                            }
                        ],
                    },
                ],
                "tasks": [
                    {
                        "title": "stringtasks",
                        "description": "string",
                        "files": [
                            {
                                "title": "string",
                                "description": "string",
                                "file": "string",
                            }
                        ],
                    },
                    {
                        "title": "stringtasks",
                        "description": "string",
                        "files": [
                            {
                                "title": "string",
                                "description": "string",
                                "file": "string",
                            }
                        ],
                    },
                ],
            }
        ]
        self.call_create_subject_section(
            id=subject.id,
            payload=data,
            print_json_response=False,
            bad_request=True,
        )

        data = [
            {
                "index": 2147483647,
                "title": "secciontest",
                "description": "string",
                "folders": [
                    {
                        "title": "string",
                        "description": "string",
                        "files": [
                            {
                                "title": "string",
                                "description": "string",
                                "file": "string",
                            }
                        ],
                    },
                    {
                        "title": "string2",
                        "description": "string",
                        "files": [
                            {
                                "title": "string",
                                "description": "string",
                                "file": "string",
                            }
                        ],
                    },
                ],
                "tasks": [
                    {
                        "title": "stringtasks",
                        "description": "string",
                        "files": [
                            {
                                "title": "string",
                                "description": "string",
                                "file": "string",
                            }
                        ],
                    },
                    {
                        "title": "stringtasks",
                        "description": "string",
                        "files": [
                            {
                                "title": "string",
                                "description": "string",
                                "file": "string",
                            }
                        ],
                    },
                ],
            }
        ]
        self.call_create_subject_section(
            id=subject.id,
            payload=data,
            print_json_response=False,
            bad_request=True,
        )

        data = [
            {
                "index": 2147483647,
                "title": "secciontest",
                "description": "string",
            },
            {
                "index": 2147483647,
                "title": "secciontest",
                "description": "string",
            },
        ]
        self.call_create_subject_section(
            id=subject.id,
            payload=data,
            print_json_response=True,
            bad_request=True,
        )
