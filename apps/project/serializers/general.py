from typing import Optional

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from ..models import (
    ROL_NAME_PROFESSOR,
    ROL_NAME_STUDENT,
    ApprovedSchoolCourse,
    Career,
    DegreeScale,
    Dropout,
    FileFolder,
    FileStudentResponse,
    Folder,
    GrantCareer,
    Professor,
    SchoolEvent,
    SchoolTask,
    SchoolYear,
    Student,
    StudentCareer,
    StudentGroup,
    StudentNote,
    StudentResponse,
    Subject,
    SubjectSection,
)
from ..utils.consts import AMOUNT_OF_CAREER_ON_BALLOT

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


class AccountCreateSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    email = serializers.EmailField()

    def validate_username(self, username):
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError(
                "Este nombre de usuario ya existe"
            )
        return username

    def validate_email(self, email):
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                "Este correo de usuario ya existe"
            )
        return email


class ProfessorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Professor
        fields = "__all__"


class ProfessorCreateSerializer(serializers.ModelSerializer):
    account = AccountCreateSerializer(write_only=True, required=False)

    class Meta:
        model = Professor
        fields = [
            "ci",
            "address",
            "last_name",
            "first_name",
            "sex",
            "account",
        ]

    def create(self, validated_data):
        account = validated_data.pop("account", None)
        if account:
            user = User.objects.create_user(**account)
            role = Group.objects.filter(name=ROL_NAME_PROFESSOR).first()
            if not role:
                role = Group.objects.create(name=ROL_NAME_PROFESSOR)
            user.groups.add(role)
            validated_data["user"] = user
        instance = super().create(validated_data)
        return instance

    def to_representation(self, instance):
        return ProfessorSerializer(instance).data


class AccountUpdateSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=False)
    password = serializers.CharField(required=False, write_only=True)
    email = serializers.EmailField(required=False)

    class Meta:
        model = User
        fields = ["username", "email", "password"]


class AccountValidateUpdateSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=False)
    password = serializers.CharField(required=False, write_only=True)
    email = serializers.EmailField(required=False)

    class Meta:
        model = User
        fields = ["username", "email", "password"]

    def validate_username(self, value):
        """Valida que el username sea único si se modifica."""
        if self.instance and self.instance.username == value:
            return value  # No hay cambio en el username
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError(
                "El nombre de usuario ya está en uso."
            )
        return value

    def validate_email(self, value):
        """Valida que el email sea único si se modifica."""
        if self.instance and self.instance.email == value:
            return value  # No hay cambio en el email
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                "El correo electrónico ya está en uso."
            )
        return value

    def update(self, instance, validated_data):
        """Actualiza los campos del usuario."""
        if "username" in validated_data:
            instance.username = validated_data["username"]
        if "email" in validated_data:
            instance.email = validated_data["email"]
        if "password" in validated_data:
            instance.set_password(validated_data["password"])
        instance.save()
        return instance


class ProfessorUpdateRequestSwaggerSerializer(serializers.ModelSerializer):
    account = AccountUpdateSerializer(write_only=True, required=False)

    class Meta:
        model = Professor
        fields = [
            "ci",
            "address",
            "last_name",
            "first_name",
            "sex",
            "account",
        ]


class ProfessorUpdateSerializer(serializers.ModelSerializer):
    account = AccountUpdateSerializer(write_only=True, required=False)

    class Meta:
        model = Professor
        fields = [
            "ci",
            "address",
            "last_name",
            "first_name",
            "sex",
            "account",
        ]

    def update(self, instance, validated_data):
        # Actualizar la cuenta asociada (si existe)
        account_data = validated_data.pop("account", None)
        if account_data is not None:
            if instance.user:  # Si ya tiene una cuenta, actualizamos
                user_serializer = AccountValidateUpdateSerializer(
                    instance.user, data=account_data, partial=True
                )
                user_serializer.is_valid(raise_exception=True)
                user_serializer.save()
            else:  # Si no tiene cuenta, creamos una nueva
                user_serializer = AccountCreateSerializer(data=account_data)
                user_serializer.is_valid(raise_exception=True)
                user = User.objects.create_user(**account_data)
                role = Group.objects.filter(name=ROL_NAME_PROFESSOR).first()
                if not role:
                    role = Group.objects.create(name=ROL_NAME_PROFESSOR)
                user.groups.add(role)
                validated_data["user"] = user
        instance = super().update(instance, validated_data)
        return instance

    def to_representation(self, instance):
        return ProfessorSerializer(instance).data


class SchoolYearSerializer(serializers.ModelSerializer):
    class Meta:
        model = SchoolYear
        fields = "__all__"

    def validate(self, attrs):
        start_date = attrs.get("start_date")
        end_date = attrs.get("end_date")
        if start_date >= end_date:
            raise serializers.ValidationError(
                "La fecha de nacimiento debe ser inferior a la fecha de fin"
            )
        return attrs


class StudentGroupRepresentationSerializer(serializers.ModelSerializer):
    professors = ProfessorSerializer(many=True)

    class Meta:
        model = StudentGroup
        fields = "__all__"


class StudentGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentGroup
        fields = "__all__"

    def to_representation(self, instance):
        return StudentGroupRepresentationSerializer(instance).data


class StudentSerializer(serializers.ModelSerializer):
    is_approved = serializers.SerializerMethodField(read_only=True)
    group = StudentGroupRepresentationSerializer()

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
            "group",
        ]

    def create(self, validated_data):
        account = validated_data.pop("account", None)
        if account:
            user = User.objects.create_user(**account)
            role = Group.objects.filter(name=ROL_NAME_STUDENT).first()
            if not role:
                role = Group.objects.create(name=ROL_NAME_STUDENT)
            user.groups.add(role)
            validated_data["user"] = user
        instance = super().create(validated_data)
        return instance

    def to_representation(self, instance):
        return StudentSerializer(instance).data


class StudentUpdateSerializer(serializers.ModelSerializer):
    account = AccountUpdateSerializer(write_only=True, required=False)

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
            "group",
        ]

    def update(self, instance, validated_data):
        # Actualizar la cuenta asociada (si existe)
        account_data = validated_data.pop("account", None)
        if account_data is not None:
            if instance.user:  # Si ya tiene una cuenta, actualizamos
                user_serializer = AccountValidateUpdateSerializer(
                    instance.user, data=account_data, partial=True
                )
                user_serializer.is_valid(raise_exception=True)
                user_serializer.save()
            else:  # Si no tiene cuenta, creamos una nueva
                user_serializer = AccountCreateSerializer(data=account_data)
                user_serializer.is_valid(raise_exception=True)
                user = User.objects.create_user(**account_data)
                role = Group.objects.filter(name=ROL_NAME_STUDENT).first()
                if not role:
                    role = Group.objects.create(name=ROL_NAME_STUDENT)
                user.groups.add(role)
                validated_data["user"] = user
        instance = super().update(instance, validated_data)
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
    professor = ProfessorSerializer(read_only=True, many=True)

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

    def validate(self, attrs):
        student: Optional[Student] = None
        if "student" in attrs:
            student = attrs["student"]
        elif self.instance:
            student = self.instance.student
        subject = attrs["subject"]
        school_year = attrs["school_year"]
        if self.instance:
            if (
                self.instance.student != student
                or self.instance.subject != subject
                or self.instance.school_year != school_year
            ):
                if StudentNote.objects.filter(
                    student=student, subject=subject, school_year=school_year
                ).exists():
                    raise serializers.ValidationError(
                        "Ya existe esta nota para este estudiante en esta asignatura en este curso"
                    )
        elif student:
            if StudentNote.objects.filter(
                student=student, subject=subject, school_year=school_year
            ).exists():
                raise serializers.ValidationError(
                    "Ya existe esta nota para este estudiante en esta asignatura en este curso"
                )

        if student and subject:
            if subject.grade > student.grade:
                raise serializers.ValidationError(
                    "La asignatura debe de ser de un grado igual o inferior al del estudiante"
                )

        return attrs

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

class DegreeScaleSimpleSerializer(serializers.ModelSerializer):

    class Meta:
        model = DegreeScale
        fields = "__all__"

class GrantCareerRepresentationSerializer(serializers.ModelSerializer):
    student = StudentSerializer(read_only=True)
    school_year = SchoolYearSerializer(read_only=True)
    career = CareerSerializer(read_only=True)
    degree_scale = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = GrantCareer
        fields = "__all__"

    @extend_schema_field(DegreeScaleSimpleSerializer)
    def get_degree_scale(self, obj):
        degree_scale=obj.get_ranking()
        if degree_scale:
            return DegreeScaleSimpleSerializer(degree_scale).data
        return None
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


class SchoolEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = SchoolEvent
        fields = "__all__"
