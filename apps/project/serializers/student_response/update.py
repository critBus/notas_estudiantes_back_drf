from rest_framework import serializers

from apps.project.models import FileStudentResponse, StudentResponse
from apps.project.utils.extenciones import get_extension


class FileStudentResponseUpdateSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        queryset=FileStudentResponse.objects.all(), required=False
    )

    class Meta:
        model = FileStudentResponse
        fields = ["id", "file", "title", "description"]


class StudentResponseUpdateSerializer(serializers.ModelSerializer):
    files = FileStudentResponseUpdateSerializer(many=True, required=False)

    class Meta:
        model = StudentResponse
        fields = ["description", "files"]

    def update(self, instance, validated_data):
        files = validated_data.pop("files", None)
        instance = super().update(instance, validated_data)
        if files is not None:
            files_ids = []
            for file_data in files:
                file_url = file_data["file"]
                file_title = file_data["title"]
                file_description = file_data["description"]
                if "id" in file_data:
                    file = file_data[
                        "id"
                    ]  # FileStudentResponse.objects.get(id=file_data["id"])
                    file.title = file_title
                    file.description = file_description
                    file.file = file_url
                    file.type = (get_extension(file_url),)
                    file.save()
                else:
                    file = FileStudentResponse.objects.create(
                        file=file_url,
                        title=file_title,
                        description=file_description,
                        type=get_extension(file_url),
                        student_response=instance,
                    )
                files_ids.append(file.id)
            FileStudentResponse.objects.filter(
                student_response=instance
            ).exclude(id__in=files_ids).delete()

        return instance
