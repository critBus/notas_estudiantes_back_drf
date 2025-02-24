from tests.professor.mixin.professor_mixin import ProfessorMixin
from tests.student.parent_case.student_test_case import StudentTestCase


class ProfessorTestCase(StudentTestCase, ProfessorMixin):
    pass
