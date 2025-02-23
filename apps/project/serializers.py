from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from .models import (
    ApprovedSchoolCourse,
    Career,
    DegreeScale,
    Dropout,
    FileFolder,
    FileStudentResponse,
    Folder,
    GrantCareer,
    Professor,
    ProfessorEvaluation,
    SchoolEvent,
    SchoolTask,
    SchoolYear,
    Student,
    StudentCareer,
    StudentNote,
    StudentResponse,
    Subject,
    SubjectSection,
)
from .utils.consts import AMOUNT_OF_CAREER_ON_BALLOT

User = get_user_model()


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


class ProfessorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Professor
        fields = "__all__"


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
            "user": {"read_only": True},
        }

    @extend_schema_field(serializers.BooleanField())
    def get_is_approved(self, obj):
        if obj:
            return obj.their_notes_are_valid()
        return False


class AccountCreateSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    email = serializers.EmailField()

    def validate_username(self, username):
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError(
                "Uste nombre de usuario ya existe"
            )
        return username

    def validate_email(self, email):
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                "Uste correo de usuario ya existe"
            )
        return email


class StudentCreateSerializer(serializers.ModelSerializer):
    account = AccountCreateSerializer(write_only=True, required=False)

    class Meta:
        model = Student
        fields = [
            "ci",
            "address",
            "grade",
            "last_name",
            "first_name",
            "registration_number",
            "sex",
            "account",
        ]

    def create(self, validated_data):
        account = validated_data.pop("account", None)
        if account:
            validated_data["user"] = User.objects.create_user(**account)
        instance = super().create(validated_data)
        return instance

    def to_representation(self, instance):
        return StudentSerializer(instance).data


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


class SubjectRepresentationSerializer(serializers.ModelSerializer):
    professor = ProfessorSerializer(read_only=True)

    class Meta:
        model = Subject
        fields = "__all__"


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = "__all__"

    def to_representation(self, instance):
        return SubjectRepresentationSerializer(instance).data


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


class ApprovedSchoolCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApprovedSchoolCourse
        fields = "__all__"

    def to_representation(self, instance):
        return ApprovedSchoolCourseRepresentationSerializer(instance).data


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


class SubjectSectionRepresentationSerializer(serializers.ModelSerializer):
    subject = SubjectRepresentationSerializer(read_only=True)
    school_year = SchoolYearSerializer(read_only=True)

    class Meta:
        model = SubjectSection
        fields = "__all__"


class SubjectSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubjectSection
        fields = "__all__"

    def to_representation(self, instance):
        return SubjectSectionRepresentationSerializer(instance).data


class FolderRepresentationSerializer(serializers.ModelSerializer):
    subject_section = SubjectSectionRepresentationSerializer(read_only=True)

    class Meta:
        model = Folder
        fields = "__all__"


class FolderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Folder
        fields = "__all__"

    def to_representation(self, instance):
        return FolderRepresentationSerializer(instance).data


class FileFolderRepresentationSerializer(serializers.ModelSerializer):
    folder = FolderRepresentationSerializer(read_only=True)

    class Meta:
        model = FileFolder
        fields = "__all__"


class FileFolderSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileFolder
        fields = "__all__"

    def to_representation(self, instance):
        return FileFolderRepresentationSerializer(instance).data


class SchoolTaskRepresentationSerializer(serializers.ModelSerializer):
    subject_section = SubjectSectionRepresentationSerializer(read_only=True)

    class Meta:
        model = SchoolTask
        fields = "__all__"


class SchoolTaskSerializer(serializers.ModelSerializer):
    subject_section = SubjectSectionRepresentationSerializer(read_only=True)

    class Meta:
        model = SchoolTask
        fields = "__all__"

    def to_representation(self, instance):
        return SchoolTaskRepresentationSerializer(instance).data


class FileSchoolTaskRepresentationSerializer(serializers.ModelSerializer):
    school_task = SchoolTaskRepresentationSerializer(read_only=True)

    class Meta:
        model = SchoolTask
        fields = "__all__"


class FileSchoolTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = SchoolTask
        fields = "__all__"

    def to_representation(self, instance):
        return FileSchoolTaskRepresentationSerializer(instance)


class StudentResponseRepresentationSerializer(serializers.ModelSerializer):
    school_task = SchoolTaskRepresentationSerializer(read_only=True)

    class Meta:
        model = StudentResponse
        fields = "__all__"


class StudentResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentResponse
        fields = "__all__"

    def to_representation(self, instance):
        return StudentResponseRepresentationSerializer(instance).data


class FileStudentResponseRepresentationSerializer(serializers.ModelSerializer):
    student_response = StudentResponseRepresentationSerializer(read_only=True)

    class Meta:
        model = FileStudentResponse
        fields = "__all__"


class FileStudentResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileStudentResponse
        fields = "__all__"

    def to_representation(self, instance):
        return FileStudentResponseRepresentationSerializer(instance).data


class ProfessorEvaluationRepresentationSerializer(serializers.ModelSerializer):
    professor = ProfessorSerializer(read_only=True)

    class Meta:
        model = ProfessorEvaluation
        fields = "__all__"


class ProfessorEvaluationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfessorEvaluation
        fields = "__all__"

    def to_representation(self, instance):
        return ProfessorEvaluationRepresentationSerializer(instance).data


class SchoolEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = SchoolEvent
        fields = "__all__"
