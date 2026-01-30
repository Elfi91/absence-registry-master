from rest_framework import serializers
from .models import Student
from core.models import Absence


class StudentAbsenceSerializer(serializers.ModelSerializer):
    """Serializer leggero per mostrare le assenze dentro lo studente"""
    class Meta:
        model = Absence
        fields = ['id', 'date', 'is_justified']


class StudentSerializer(serializers.ModelSerializer):
    absences = StudentAbsenceSerializer(many=True, read_only=True)

    class Meta:
        model = Student
        fields = ['id', 'first_name', 'last_name', 'course', 'absences']

