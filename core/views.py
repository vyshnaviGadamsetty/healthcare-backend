from rest_framework import viewsets, permissions, generics
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Patient, Doctor, PatientDoctor
from .serializers import (
    PatientSerializer,
    DoctorSerializer,
    PatientDoctorSerializer,
    RegisterSerializer
)

# 👤 User Registration View
class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]


# 🧑‍⚕️ Patient Views
class PatientViewSet(viewsets.ModelViewSet):
    serializer_class = PatientSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # only return patients created by the logged-in user
        return Patient.objects.filter(created_by=self.request.user).order_by('-created_at')

    def perform_create(self, serializer):
        # automatically link patient to current user
        serializer.save(created_by=self.request.user)


# 👩‍⚕️ Doctor Views
class DoctorViewSet(viewsets.ModelViewSet):
    queryset = Doctor.objects.all().order_by('-created_at')
    serializer_class = DoctorSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


# 🔗 Patient–Doctor Mapping Views
class PatientDoctorViewSet(viewsets.ModelViewSet):
    queryset = PatientDoctor.objects.select_related('patient', 'doctor').order_by('-created_at')
    serializer_class = PatientDoctorSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx['request'] = self.request
        return ctx

    @action(detail=False, methods=['get'], url_path=r'(?P<patient_id>\d+)')
    def list_for_patient(self, request, patient_id=None):
        # return all mappings for a specific patient
        qs = self.get_queryset().filter(patient_id=patient_id)
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)
