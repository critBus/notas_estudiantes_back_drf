import random
from typing import Optional

from django.contrib.auth import get_user_model
from faker import Faker

from apps.project.models import Professor

User = get_user_model()
fake = Faker()


class ProfessorMixin:
    def create_random_professor(
        self,
        user: Optional[User] = None,
    ) -> Professor:
        return Professor.objects.create(
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            ci=fake.unique.numerify(text="############")[:11],
            address=fake.address(),
            sex=random.choice(["M", "F"]),
            user=user,
        )
