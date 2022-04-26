from rest_framework import serializers


class PaymentCourseSerializer(serializers.Serializer):
    course_pre = serializers.IntegerField()
    course_transco = serializers.IntegerField()
    inscription = serializers.IntegerField()