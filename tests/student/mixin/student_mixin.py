import random
from typing import Optional

from django.contrib.auth import get_user_model
from faker import Faker

from apps.project.models import Student

User = get_user_model()
fake = Faker()


class StudentMixin:
    def create_random_student(
        self,
        grade: Optional[int] = None,
        is_graduated=False,
        is_dropped_out=False,
        user: Optional[User] = None,
    ) -> Student:
        return Student.objects.create(
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            ci=fake.unique.numerify(text="############")[:11],
            address=fake.address(),
            grade=grade if grade else random.choice([7, 8, 9]),
            registration_number=fake.unique.numerify(text="############")[:11],
            sex=random.choice(["M", "F"]),
            is_graduated=is_graduated
            if is_graduated is not None
            else random.choices([True, False]),
            is_dropped_out=is_dropped_out
            if is_dropped_out is not None
            else random.choices([True, False]),
            user=user,
        )
