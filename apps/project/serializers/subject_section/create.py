from rest_framework import serializers

from apps.project.models import (
    FileFolder,
    FileSchoolTask,
    Folder,
    SchoolTask,
    SubjectSection,
)


class FileFolderSubjectSectionSerializer(serializers.ModelSerializer):
    file = serializers.CharField()

    class Meta:
        model = FileFolder
        fields = ["id", "title", "description", "file"]


class FolderSubjectSectionSerializer(serializers.ModelSerializer):
    files = FileFolderSubjectSectionSerializer(many=True, required=False)

    class Meta:
        model = Folder
        fields = ["id", "title", "description", "files"]


class FileSchoolTaskSubjectSectionSerializer(serializers.ModelSerializer):
    file = serializers.CharField()

    class Meta:
        model = FileSchoolTask
        fields = ["id", "title", "description", "file"]


class SchoolTaskSubjectSectionSerializer(serializers.ModelSerializer):
    files = FileSchoolTaskSubjectSectionSerializer(many=True, required=False)

    class Meta:
        model = SchoolTask
        fields = ["id", "title", "description", "files"]


class SubjectSectionCreateSerializer(serializers.ModelSerializer):
    folders = FolderSubjectSectionSerializer(many=True, required=False)
    tasks = SchoolTaskSubjectSectionSerializer(many=True, required=False)

    class Meta:
        model = SubjectSection
        fields = ["id", "index", "title", "description", "folders", "tasks"]
