from tests.student.parent_case.student_test_case import StudentTestCase
from tests.subject_section.mixin.subject_section_mixin import (
    SubjectSectionMixin,
)


class SubjectSectionTestCase(StudentTestCase, SubjectSectionMixin):
    pass
