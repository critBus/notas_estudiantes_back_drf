from rest_framework import serializers


class SchoolStatisticsSerializer(serializers.Serializer):
    amount_of_students = serializers.IntegerField()
    amount_of_students_7 = serializers.IntegerField()
    amount_of_students_8 = serializers.IntegerField()
    amount_of_students_9 = serializers.IntegerField()
    amount_of_professor = serializers.IntegerField()
    dropouts_7 = serializers.IntegerField()
    dropouts_8 = serializers.IntegerField()
    dropouts_9 = serializers.IntegerField()
    not_approved_7 = serializers.IntegerField()
    not_approved_8 = serializers.IntegerField()
    not_approved_9 = serializers.IntegerField()
