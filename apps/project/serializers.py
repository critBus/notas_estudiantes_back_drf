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


class SchoolYearSerializer(serializers.ModelSerializer):
    class Meta:
        model = SchoolYear
        fields = "__all__"


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = "__all__"  # Incluye todos los campos del modelo


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
