from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from .models import (
    Award,
    Career,
    Dropout,
    Graduation,
    GraduationGrade,
    SchoolYear,
    Student,
    StudentCareer,
    StudentNote,
    Subject,
)


class ErrorSerializer(serializers.Serializer):
    error = serializers.CharField()


class BallotCreateSerializer(serializers.Serializer):
    list_career_name = serializers.ListField(child=serializers.CharField())

    def validate_list_career_name(self, value):
        list_career = []
        if len(list(set(value))) != 10:
            raise serializers.ValidationError(
                "La cantidad de carreras debe ser un total de 10"
            )
        for career_name in value:
            career = Career.objects.filter(name=career_name).first()
            if career is None:
                raise serializers.ValidationError(
                    f"No existe la carrera con el nombre {career}"
                )
        return list_career


class SchoolYearSerializer(serializers.ModelSerializer):
    class Meta:
        model = SchoolYear
        fields = "__all__"


class StudentSerializer(serializers.ModelSerializer):
    is_approved = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Student
        fields = "__all__"  # Incluye todos los campos del modelo

    @extend_schema_field(serializers.BooleanField())
    def get_is_approved(self, obj):
        if obj:
            return obj.their_notes_are_valid()
        return False


class StudentBallotSerializer(StudentSerializer):
    ballot = serializers.SerializerMethodField(read_only=True)

    @extend_schema_field(serializers.ListField(child=serializers.CharField()))
    def get_ballot(self, obj):
        if obj:
            return obj.get_ballot()
        return []


class DropoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dropout
        fields = "__all__"


class CareerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Career
        fields = "__all__"


class GraduationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Graduation
        fields = "__all__"


class GraduationGradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = GraduationGrade
        fields = "__all__"


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = "__all__"


class StudentNoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentNote
        fields = "__all__"


class AwardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Award
        fields = "__all__"


class StudentCareerSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentCareer
        fields = "__all__"
