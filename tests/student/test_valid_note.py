from django.contrib.auth import get_user_model

User = get_user_model()
# class TestValidNote(StudentTestCase):
#     def test_is_valid_note(self):
#         course = SchoolYear.get_current_course()
#         subject=self.subjects[0]
#         student = self.create_random_student(grade=9)
#         nota = StudentNote.objects.create(
#             subject=subject, student=student, school_year=course
#         )
#         nota.tcp1 = random.randint(30, 40)
#         nota.tcp2 = random.randint(30, 40)
#         nota.asc = random.randint(6, 10)
#         nota.final_exam = random.randint(60, 100)
#         nota.calculate_final_grade()
#         nota.save()
