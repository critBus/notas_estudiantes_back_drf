from datetime import timedelta
from typing import List

from django.utils import timezone

from apps.project.models import SchoolYear


class SchoolYearMixin:
    def create_current_school_year(self) -> SchoolYear:
        return SchoolYear.objects.create(
            name="2025-2026",
            start_date=timezone.now().date(),
            end_date=(timezone.now() + timedelta(days=365)).date(),
        )

    def create_3_school_year(self, start_year: int) -> List[SchoolYear]:
        school_years = []
        for i in range(3):
            first_year = start_year + i
            end_year = first_year + 1
            start_date = timezone.now().date()
            start_date = start_date.replace(year=first_year)
            end_date = timezone.now().date()
            end_date = end_date.replace(year=end_year)
            school_years.append(
                SchoolYear.objects.create(
                    name=f"{first_year}-{end_year}",
                    start_date=start_date,
                    end_date=end_date,
                )
            )
        return school_years
