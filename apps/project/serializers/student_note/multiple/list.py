from rest_framework import serializers

from apps.project.models import StudentNote


class StudentNoteSimpleMultipleSerializer(serializers.ModelSerializer):
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
