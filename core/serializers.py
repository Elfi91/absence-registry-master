from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Absence
from students.serializers import StudentSerializer
from django.contrib.auth.password_validation import validate_password

# Questo mancava nel file che abbiamo aggiornato prima!
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
        fields = ['id', 'student', 'student_details', 'date', 'is_justified', 'comment', 'created_by']
        read_only_fields = ['created_by']

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, validators=[validate_password])

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("La vecchia password non è corretta.")
        return value