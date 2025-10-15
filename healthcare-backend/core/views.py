from rest_framework import viewsets, permissions, generics, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import Patient, Doctor, PatientDoctor
from .serializers import (
    PatientSerializer,
    DoctorSerializer,
    PatientDoctorSerializer,
    RegisterSerializer
)

User = get_user_model()

# 🔐 Custom Token Serializer to include role and username
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
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


# 🔐 Custom Login View
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


# 👤 User Registration View
class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        user = User.objects.get(username=request.data['username'])
        return Response({
            "detail": "User registered successfully",
            "username": user.username,
            "role": user.profile.role
        }, status=status.HTTP_201_CREATED)


# 🧑‍⚕️ Patient Views
class PatientViewSet(viewsets.ModelViewSet):
    serializer_class = PatientSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.profile.role == 'admin':
            # Admin can see all patients
            return Patient.objects.all().order_by('-created_at')
        # Patients can only see their own records
        return Patient.objects.filter(created_by=user).order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def destroy(self, request, *args, **kwargs):
        # ❌ Patients can't delete
        if request.user.profile.role != 'admin':
            return Response(
                {"detail": "Not authorized to delete patients."},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().destroy(request, *args, **kwargs)


# 👩‍⚕️ Doctor Views
class DoctorViewSet(viewsets.ModelViewSet):
    queryset = Doctor.objects.all().order_by('-created_at')
    serializer_class = DoctorSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def destroy(self, request, *args, **kwargs):
        # ❌ Patients can't delete doctors
        if request.user.profile.role != 'admin':
            return Response(
                {"detail": "Not authorized to delete doctors."},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().destroy(request, *args, **kwargs)


# 🔗 Patient–Doctor Mapping Views
class PatientDoctorViewSet(viewsets.ModelViewSet):
    queryset = PatientDoctor.objects.select_related('patient', 'doctor').order_by('-created_at')
    serializer_class = PatientDoctorSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx['request'] = self.request
        return ctx

    @action(detail=False, methods=['get'], url_path=r'patient/(?P<patient_id>\d+)')
    def list_for_patient(self, request, patient_id=None):
        qs = self.get_queryset().filter(patient_id=patient_id)
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)

