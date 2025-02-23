from django.contrib.auth import get_user_model

from tests.student.parent_case.student_test_case import StudentTestCase

User = get_user_model()


class TestStudentAccount(StudentTestCase):
    def test_student_account(self):
        user = User.objects.create_user(
            username="test", email="test@gmail.com", password="123"
        )
        student = self.create_random_student(user=user)
        self.assertEqual(user.first_name, student.first_name)
        self.assertEqual(user.last_name, student.last_name)

        student.first_name = "edit1"
        student.last_name = "edit2"
        student.save()
        self.assertEqual(user.first_name, student.first_name)
        self.assertEqual(user.last_name, student.last_name)

        self.assertTrue(User.objects.filter(id=user.id).exists())
        student.delete()
        self.assertFalse(User.objects.filter(id=user.id).exists())
