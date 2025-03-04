from rest_framework import serializers

from apps.project.models import (
    FileFolder,
    FileSchoolTask,
    Folder,
    SchoolTask,
    SubjectSection,
)


class FileFolderSubjectSectionSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        queryset=FileFolder.objects.all(), required=False
    )
    file = serializers.CharField()

    class Meta:
        model = FileFolder
        fields = ["id", "title", "description", "file"]


class FolderSubjectSectionSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        queryset=Folder.objects.all(), required=False
    )
    files = FileFolderSubjectSectionSerializer(many=True, required=False)

    class Meta:
        model = Folder
        fields = ["id", "title", "description", "files"]


class FileSchoolTaskSubjectSectionSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        queryset=FileSchoolTask.objects.all(), required=False
    )
    file = serializers.CharField()

    class Meta:
        model = FileSchoolTask
        fields = ["id", "title", "description", "file"]


class SchoolTaskSubjectSectionSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        queryset=SchoolTask.objects.all(), required=False
    )
    files = FileSchoolTaskSubjectSectionSerializer(many=True, required=False)

    class Meta:
        model = SchoolTask
        fields = ["id", "title", "description", "files"]


class SubjectSectionCreateSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        queryset=SubjectSection.objects.all(), required=False
    )
    folders = FolderSubjectSectionSerializer(many=True, required=False)
    tasks = SchoolTaskSubjectSectionSerializer(many=True, required=False)

    class Meta:
        model = SubjectSection
        fields = ["id", "index", "title", "description", "folders", "tasks"]
