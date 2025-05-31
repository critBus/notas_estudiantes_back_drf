from rest_framework import serializers

from apps.project.models import StudentNote,Subject,SchoolYear

class SchoolYearInMultipleSerializer(serializers.ModelSerializer):
    class Meta:
        model = SchoolYear
        fields = "__all__"

class SubjectInMultipleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = "__all__"

class StudentNoteSimpleMultipleByStudentSerializer(serializers.ModelSerializer):
    subject=SubjectInMultipleSerializer()
    school_year=SchoolYearInMultipleSerializer()
    class Meta:
        model = StudentNote
        fields = [
            "id",
            "student",
            "subject",
            "school_year",
            "asc",
            "final_exam",
            "tcp1",
            "tcp2",
        ]
