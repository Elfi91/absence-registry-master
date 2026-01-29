from rest_framework import serializers
from .models import Student
from core.models import Absence

class StudentAbsenceSerializer(serializers.ModelSerializer):
    """Serializer leggero per mostrare le assenze dentro lo studente"""
    class Meta:
        model = Absence
        fields = ['id', 'date', 'is_justified', 'comment']

class StudentSerializer(serializers.ModelSerializer):
    # 'absences' è il related_name che hai nel modello Absence
    absences = StudentAbsenceSerializer(many=True, read_only=True)

    # Da qui possiamo leggere la @property che abbiamo inserito in models.py
    presence_percentage = serializers.ReadOnlyField()

    class Meta:
        model = Student
        fields = ['id', 'first_name', 'last_name', 'classroom', 'absences', 'presence_percentage']