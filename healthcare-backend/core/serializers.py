from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import Patient, Doctor, PatientDoctor

User = get_user_model()

# 🧾 REGISTER SERIALIZER
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    role = serializers.CharField(read_only=True)  # include role in response

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'role']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password']
        )
        # UserProfile is auto-created by signal
        return user

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['role'] = instance.profile.role  # 👈 get role from UserProfile
        rep['detail'] = "User registered successfully"
        return rep


# 🔐 CUSTOM LOGIN TOKEN SERIALIZER (to include role in login)
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['role'] = user.profile.role
        token['username'] = user.username
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        data['role'] = self.user.profile.role
        data['username'] = self.user.username
        return data


# 🧑‍⚕️ PATIENT SERIALIZER
class PatientSerializer(serializers.ModelSerializer):
    created_by = serializers.ReadOnlyField(source='created_by.id')

    class Meta:
        model = Patient
        fields = ('id', 'name', 'age', 'disease', 'created_by', 'created_at', 'updated_at')


# 🩺 DOCTOR SERIALIZER
class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = ('id', 'name', 'specialization', 'created_at', 'updated_at')


# 🔗 PATIENT–DOCTOR MAPPING SERIALIZER
# serializers.py
class PatientDoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientDoctor
        fields = ('id', 'patient', 'doctor', 'created_at')

    def validate(self, attrs):
        request = self.context.get('request')
        patient = attrs.get('patient')

        # 👑 allow admin to map anyone
        if request.user.profile.role != 'admin' and request.user != patient.created_by:
            raise serializers.ValidationError('You can only map doctors to your own patients.')
        return attrs

