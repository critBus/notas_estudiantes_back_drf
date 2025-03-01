from rest_framework import serializers

from apps.project.models import FileStudentResponse, StudentResponse


class FileStudentResponseUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileStudentResponse
        fields = ["file", "title", "description"]


class StudentResponseUpdateSerializer(serializers.ModelSerializer):
    files = FileStudentResponseUpdateSerializer(many=True, required=False)

    class Meta:
        model = StudentResponse
        fields = "__all__"

    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)
        return instance
