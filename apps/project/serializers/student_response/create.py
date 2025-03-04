from rest_framework import serializers

from apps.project.models import FileStudentResponse, StudentResponse
from apps.project.serializers.general import (
    StudentResponseRepresentationSerializer,
)
from apps.project.utils.extenciones import get_extension


class FileStudentResponseCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileStudentResponse
        fields = ["file", "title", "description"]


class StudentResponseCreateSerializer(serializers.ModelSerializer):
    files = FileStudentResponseCreateSerializer(many=True, required=False)

    class Meta:
        model = StudentResponse
        fields = ["date", "description", "student", "school_task", "files"]

    def create(self, validated_data):
        files = validated_data.pop("files", None)

        instance = super().create(validated_data)
        if files:
            for file_data in files:
                file_url = file_data["file"]
                file_title = file_data["title"]
                file_description = file_data["description"]

                file = FileStudentResponse()
                file.title = file_title
                file.description = file_description
                file.file = file_url
                file.type = get_extension(file_url)
                file.student_response = instance
                file.save()

            # user = User.objects.create_user(**account)
            # role = Group.objects.filter(name=ROL_NAME_STUDENT).first()
            # if not role:
            #     role = Group.objects.create(name=ROL_NAME_STUDENT)
            # user.groups.add(role)
            # validated_data["user"] = user
        return instance

    def to_representation(self, instance):
        return StudentResponseRepresentationSerializer(instance).data
