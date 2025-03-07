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

    def validate(self, attrs):
        section_title = attrs["title"]
        folders = attrs.get("folders", None)
        tasks = attrs.get("tasks", None)

        if folders:
            folders_titles = []
            for data_folder in folders:
                title = data_folder["title"]
                if title in folders_titles:
                    raise serializers.ValidationError(
                        f"Hay carpetas con nombres repetidos en la seccion {section_title}: {title}"
                    )
                folders_titles.append(title)

        if tasks:
            tasks_titles = []
            for data_task in tasks:
                title = data_task["title"]
                if title in tasks_titles:
                    raise serializers.ValidationError(
                        f"Hay tareas con nombres repetidos en la seccion {section_title}: {title}"
                    )
                tasks_titles.append(title)
        return attrs
