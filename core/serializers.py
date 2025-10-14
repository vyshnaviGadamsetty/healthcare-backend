from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from .models import Patient, Doctor, PatientDoctor

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    def validate_password(self, value):
        validate_password(value)
        return value

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class PatientSerializer(serializers.ModelSerializer):
    created_by = serializers.ReadOnlyField(source='created_by.id')

    class Meta:
        model = Patient
        fields = ('id', 'name', 'age', 'disease', 'created_by', 'created_at', 'updated_at')


class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = ('id', 'name', 'specialization', 'created_at', 'updated_at')


class PatientDoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientDoctor
        fields = ('id', 'patient', 'doctor', 'created_at')

    def validate(self, attrs):
        request = self.context.get('request')
        patient = attrs.get('patient')
        if request and request.user != patient.created_by:
            raise serializers.ValidationError('You can only map doctors to your own patients.')
        return attrs
