from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Absence
from students.serializers import StudentSerializer
from students.models import Student
from django.contrib.auth.password_validation import validate_password
from datetime import date


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'email')

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email'),
            password=validated_data['password']
        )
        return user


class AbsenceSerializer(serializers.ModelSerializer):
    student_details = StudentSerializer(source='student', read_only=True)

    class Meta:
        model = Absence
        fields = ['id', 'student', 'student_details', 'date', 'is_justified', 'created_by']
        read_only_fields = ['created_by']

    def validate_student(self, value):
        """
        Valida che lo studente esista nel database
        """
        if not Student.objects.filter(id=value.id).exists():
            raise serializers.ValidationError(
                f"Lo studente con ID {value.id} non è presente nel sistema"
            )
        return value

    def validate_date(self, value):
        """
        Si accerta della validità della data dell'assenza
        """
        if value > date.today():
            raise serializers.ValidationError(
                "Non è possibile registrare l'assenza per una data futura"
            )
        return value

    def validate_comment(self, value):
        """
        Pulisce e valida
        """
        if value:
            value = value.strip()

            if len(value) > 500:
                raise serializers.ValidationError(
                    "Non è possibile superare i 500 caratteri"
                )

        return value

    def validate(self, data):
        """
        Validazione completa: evita duplicati
        """
        student = data.get('student')
        absence_date = data.get('date')

        # è già presente un'assenza per questo id in questa data
        # in caso di aggiornamento (self.instance esiste), si esclude l'assenza corrente
        if self.instance:
            existing = Absence.objects.filter(
                student=student,
                date=absence_date
            ).exclude(id=self.instance.id)
        else:
            existing = Absence.objects.filter(
                student=student,
                date=absence_date
            )

        if existing.exists():
            raise serializers.ValidationError(
                f"E' già registrata un'assenza per {student.first_name} {student.last_name} "
                f"in data {absence_date}"
            )

        return data


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, validators=[validate_password])

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("La password non è corretta.")
        return value