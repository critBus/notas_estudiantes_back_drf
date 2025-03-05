from rest_framework import serializers

from apps.project.models import StudentNote
from apps.project.serializers.general import StudentNoteRepresentationSerializer


class StudentNoteCreateMultipleSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        queryset=StudentNote.objects.all(), required=False
    )

    class Meta:
        model = StudentNote
        fields = [
            "id",
            "student",
            "subject",
            "asc",
            "final_exam",
            "tcp1",
            "tcp2",
        ]

    def to_representation(self, instance):
        return StudentNoteRepresentationSerializer(instance).data
