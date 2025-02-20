from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from .models import (
    ApprovedSchoolCourse,
    Career,
    DegreeScale,
    Dropout,
    GrantCareer,
    SchoolYear,
    Student,
    StudentCareer,
    StudentNote,
    Subject,
)
from .utils.consts import AMOUNT_OF_CAREER_ON_BALLOT


class ErrorSerializer(serializers.Serializer):
    error = serializers.CharField()


class BallotCreateSerializer(serializers.Serializer):
    list_career_name = serializers.ListField(child=serializers.CharField())

    def validate_list_career_name(self, value):
        list_career = []
        size = len(value)
        reduce = len(list(set(value)))
        if reduce != size:
            raise serializers.ValidationError("Hay carreras repetidas")
        if reduce != AMOUNT_OF_CAREER_ON_BALLOT:
            raise serializers.ValidationError(
                f"La cantidad de carreras debe ser un total de {AMOUNT_OF_CAREER_ON_BALLOT}"
            )
        for career_name in value:
            career = Career.objects.filter(name=career_name).first()
            if career is None:
                raise serializers.ValidationError(
                    f"No existe la carrera con el nombre {career_name}"
                )
            list_career.append(career)
        return list_career


class SchoolYearSerializer(serializers.ModelSerializer):
    class Meta:
        model = SchoolYear
        fields = "__all__"


class StudentSerializer(serializers.ModelSerializer):
    is_approved = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Student
        fields = "__all__"
        extra_kwargs = {
            "is_graduated": {"read_only": True},
            "is_dropped_out": {"read_only": True},
        }

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


class CareerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Career
        fields = "__all__"


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = "__all__"


class StudentNoteRepresentationSerializer(serializers.ModelSerializer):
    student = StudentSerializer(read_only=True)
    subject = SubjectSerializer(read_only=True)
    school_year = SchoolYearSerializer(read_only=True)

    class Meta:
        model = StudentNote
        fields = "__all__"


class StudentNoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentNote
        fields = "__all__"

    def to_representation(self, instance):
        return StudentNoteRepresentationSerializer(instance).data


class StudentCareerSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentCareer
        fields = "__all__"


class DegreeScaleSerializer(serializers.ModelSerializer):
    student = StudentSerializer(read_only=True)
    school_year = SchoolYearSerializer(read_only=True)

    class Meta:
        model = DegreeScale
        fields = "__all__"


class ApprovedSchoolCourseRepresentationSerializer(serializers.ModelSerializer):
    student = StudentSerializer(read_only=True)
    school_year = SchoolYearSerializer(read_only=True)

    class Meta:
        model = ApprovedSchoolCourse
        fields = "__all__"


class GrantCareerRepresentationSerializer(serializers.ModelSerializer):
    student = StudentSerializer(read_only=True)
    approved_school_course = ApprovedSchoolCourseRepresentationSerializer(
        read_only=True
    )
    career = CareerSerializer(read_only=True)

    class Meta:
        model = GrantCareer
        fields = "__all__"


class GrantCareerSerializer(serializers.ModelSerializer):
    class Meta:
        model = GrantCareer
        fields = "__all__"

    def to_representation(self, instance):
        return GrantCareerRepresentationSerializer(instance).data


class DropoutRepresentationSerializer(serializers.ModelSerializer):
    student = StudentSerializer(read_only=True)

    class Meta:
        model = Dropout
        fields = "__all__"


class DropoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dropout
        fields = "__all__"

    def to_representation(self, instance):
        return DropoutRepresentationSerializer(instance).data
