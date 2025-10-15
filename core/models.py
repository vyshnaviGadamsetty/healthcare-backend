
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Timestamped(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True  # This means no table is created for this model

class Patient(Timestamped):
    name = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    disease = models.CharField(max_length=200, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='patients')

    def __str__(self):
        return self.name

class Doctor(Timestamped):
    name = models.CharField(max_length=100)
    specialization = models.CharField(max_length=120)

    def __str__(self):
        return f"{self.name} ({self.specialization})"

class PatientDoctor(Timestamped):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='doctor_links')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='patient_links')

    class Meta:
        unique_together = ('patient', 'doctor')
