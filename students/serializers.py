from rest_framework import serializers
from .models import Student
from core.models import Absence

class StudentAbsenceSerializer(serializers.ModelSerializer):
    """
    Serializer 'leggero': serve solo per elencare le assenze
    quando visualizziamo i dettagli di uno studente.
    """
    class Meta:
        model = Absence
        fields = ['id', 'date', 'is_justified']

class StudentSerializer(serializers.ModelSerializer):
    """
    Serializer principale dello Studente.
    Trasforma il modello Python in JSON per le API.
    """

    # NESTED SERIALIZER (Serializzatore Nidificato):
    # Invece di mostrare solo gli ID delle assenze, usiamo il serializer qui sopra
    # per mostrare la lista completa dei dettagli (data, giustificazione) dentro lo studente.
    # many=True: perché uno studente può avere molte assenze.
    # read_only=True: le assenze si creano dal loro endpoint, non da qui.
    absences = StudentAbsenceSerializer(many=True, read_only=True)

    # CAMPO CALCOLATO:
    # Qui diciamo a Django Rest Framework di leggere la funzione @property
    # 'presence_percentage' che abbiamo scritto nel models.py e includerla nel JSON.
    presence_percentage = serializers.ReadOnlyField()

    class Meta:
        model = Student
        fields = ['id', 'first_name', 'last_name', 'course', 'absences', 'presence_percentage']