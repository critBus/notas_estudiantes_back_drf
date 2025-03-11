from rest_framework import serializers


class SchoolStatisticsSerializer(serializers.Serializer):
    amount_of_students = serializers.IntegerField()
    amount_of_students_7 = serializers.IntegerField()
    amount_of_students_8 = serializers.IntegerField()
    amount_of_students_9 = serializers.IntegerField()
    amount_of_professor = serializers.IntegerField()
