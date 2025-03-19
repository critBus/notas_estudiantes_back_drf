from rest_framework import serializers

from apps.project.models import SchoolYear


class NewSchoolYearSerializer(serializers.ModelSerializer):
    class Meta:
        model = SchoolYear
        fields = "__all__"

    def validate_start_date(self, start_date):
        if SchoolYear.objects.filter(start_date__gte=start_date).exists():
            raise serializers.ValidationError(
                "La fecha de incio tiene que ser mas reciente que la de los cursos existentes"
            )
        return start_date

    def validate(self, attrs):
        start_date = attrs.get("start_date")
        end_date = attrs.get("end_date")
        if start_date >= end_date:
            raise serializers.ValidationError(
                "La fecha de nacimiento debe ser inferior a la fecha de fin"
            )
        return attrs
