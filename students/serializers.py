from rest_framework import serializers
from .models import Student
from core.models import Absence

class StudentAbsenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Absence
        fields = ['id', 'date', 'is_justified',]


class StudentSerializer(serializers.ModelSerializer):
    absences = StudentAbsenceSerializer(many=True, read_only=True)

    class Meta:
        model = Student
        fields = ['id', 'first_name', 'last_name', 'course', 'matricola', 'absences']
        read_only_fields = ['matricola']  # La matricola si genera automaticamente

    def validate_first_name(self, value):
        """Validazione del nome: non può essere vuoto e deve essere capitalizzato"""
        print(value)

        if not value.strip():
            raise serializers.ValidationError("La risposta non è valida")

        return value.capitalize()

    def validate_last_name(self, value):
        """Validazione del cognome: il campo non può essere vuoto"""
        if not value.strip():
            raise serializers.ValidationError("La risposta non è valida")

        return value.capitalize()

    def validate_course(self, value):
        """Validazione del corso: tipo DEV, DSGN, PHOTOGRPH, WEB, etc"""
        if not value.strip():
            raise serializers.ValidationError("La risposta non è valida")

        value = value.strip().upper().replace(" ", "")

        # Verifica che sia un codice valido (lettere, 2-10 caratteri)
        if not value.isalpha() or len(value) < 2 or len(value) > 10:
            raise serializers.ValidationError(
                "Il corso deve essere un codice di 2-10 lettere (es: DEV, DSGN, PHOTOGRPH, WEB, etc)"
            )

        return value

    def validate(self, data):
        """
        Validazione generale: la matricola unica previene duplicati
        """
        instance = self.instance

        first_name = data.get('first_name', instance.first_name if instance else None)
        last_name = data.get('last_name', instance.last_name if instance else None)
        course = data.get('course', instance.course if instance else None)

     # Se stiamo aggiornando (self.instance esiste), escludiamo lo studente corrente
        if not (first_name and last_name and course):
            return data

        # CONTROLLO DUPLICATI NEL DATABASE:
        # ricerca di studentx con lo stesso nome, cognome e corso.
        # Uso di 'iexact' per rendere la ricerca "Case Insensitive"

        duplicates = Student.objects.filter(
            first_name__iexact=first_name,
            last_name__iexact=last_name,
            course__iexact=course
        )

        if instance:
            duplicates = duplicates.exclude(id=instance.id)

        if duplicates.exists():
            raise serializers.ValidationError(
                "Esiste già uno studente con questo nome e cognome in questo corso."
            )

        return data