from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from apps.project.models import (
    FileFolder,
    FileSchoolTask,
    FileStudentResponse,
    Folder,
    SchoolTask,
    StudentResponse,
    SubjectSection,
)
from apps.project.serializers.general import StudentSerializer


class FileFolderSubjectSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileFolder
        fields = ["id", "title", "description", "file"]


class FolderSubjectSectionSerializer(serializers.ModelSerializer):
    files = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Folder
        fields = ["id", "title", "description", "files"]

    @extend_schema_field(
        FileFolderSubjectSectionSerializer(many=True, read_only=True)
    )
    def get_files(self, instance):
        if instance:
            q = FileFolder.objects.filter(folder=instance).order_by("pk")
            return FileFolderSubjectSectionSerializer(q, many=True).data
        return instance


class FileSchoolTaskInSubjectSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileSchoolTask
        fields = ["id", "title", "description", "file"]


class FileStudentResponseSubjectSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileStudentResponse
        fields = ["id", "title", "description", "file"]


class StudentResponseSubjectSectionSerializer(serializers.ModelSerializer):
    files = serializers.SerializerMethodField(read_only=True)
    student = StudentSerializer()

    class Meta:
        model = StudentResponse
        fields = ["id", "student", "description", "files"]

    @extend_schema_field(
        FileStudentResponseSubjectSectionSerializer(many=True, read_only=True)
    )
    def get_files(self, instance):
        if instance:
            q = FileStudentResponse.objects.filter(
                student_response=instance
            ).order_by("pk")
            return FileStudentResponseSubjectSectionSerializer(
                q, many=True
            ).data
        return instance


class SchoolTaskInSubjectSectionSerializer(serializers.ModelSerializer):
    files = serializers.SerializerMethodField(read_only=True)
    students_responses = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = SchoolTask
        fields = ["id", "title", "description", "files", "students_responses"]

    @extend_schema_field(
        FileSchoolTaskInSubjectSectionSerializer(many=True, read_only=True)
    )
    def get_files(self, instance):
        if instance:
            q = FileSchoolTask.objects.filter(school_task=instance).order_by(
                "pk"
            )
            return FileSchoolTaskInSubjectSectionSerializer(q, many=True).data
        return instance

    @extend_schema_field(
        StudentResponseSubjectSectionSerializer(many=True, read_only=True)
    )
    def get_students_responses(self, instance):
        if instance:
            q = StudentResponse.objects.filter(school_task=instance).order_by(
                "date"
            )
            return StudentResponseSubjectSectionSerializer(q, many=True).data
        return instance


class SubjectSectionCreateRepresentationSerializer(serializers.ModelSerializer):
    folders = serializers.SerializerMethodField(read_only=True)
    tasks = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = SubjectSection
        fields = ["id", "index", "title", "description", "folders", "tasks"]

    @extend_schema_field(
        FolderSubjectSectionSerializer(many=True, read_only=True)
    )
    def get_folders(self, instance):
        if instance:
            q = Folder.objects.filter(subject_section=instance).order_by("pk")
            return FolderSubjectSectionSerializer(q, many=True).data
        return instance

    @extend_schema_field(
        SchoolTaskInSubjectSectionSerializer(many=True, read_only=True)
    )
    def get_tasks(self, instance):
        if instance:
            q = SchoolTask.objects.filter(subject_section=instance).order_by(
                "date"
            )
            return SchoolTaskInSubjectSectionSerializer(q, many=True).data
        return instance
