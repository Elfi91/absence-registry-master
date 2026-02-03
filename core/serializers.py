from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Absence
from students.serializers import StudentSerializer
from django.contrib.auth.password_validation import validate_password

class RegisterSerializer(serializers.ModelSerializer):
    """Gestisce la registrazione di nuovi utenti (Admin/Docenti)."""
    # write_only=True assicura che la password non venga mai restituita nella risposta API
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'email')

    def create(self, validated_data):
        # Sovrascriviamo il metodo create standard per usare 'create_user'.
        # Questo è FONDAMENTALE perché si occupa di criptare (hashare) la password
        # invece di salvarla in chiaro nel database.
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email'),
            password=validated_data['password']
        )
        return user

class AbsenceSerializer(serializers.ModelSerializer):
    """Serializer per visualizzare e creare assenze."""

    # Nested Serializer: Invece di mostrare solo l'ID dello studente (es. "student": 1),
    # mostriamo l'oggetto completo (Nome, Cognome, Corso) in sola lettura.
    student_details = StudentSerializer(source='student', read_only=True)

    class Meta:
        model = Absence
        # Includiamo 'student_details' per la lettura e 'student' (ID) per la scrittura
        fields = ['id', 'student', 'student_details', 'date', 'is_justified', 'created_by']
        # created_by è read_only perché viene impostato automaticamente dal backend (vedi views.py)
        read_only_fields = ['created_by']

class ChangePasswordSerializer(serializers.Serializer):
    """Gestisce il cambio password verificando che la vecchia sia corretta."""
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, validators=[validate_password])

    def validate_old_password(self, value):
        # Controllo di sicurezza: verifica che la vecchia password inserita
        # corrisponda a quella attuale dell'utente loggato.
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("La vecchia password non è corretta.")
        return value