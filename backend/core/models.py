from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver


User = get_user_model()

# 🕒 Common timestamp fields
class Timestamped(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True  # No table is created for this model

# 🧑‍⚕️ Patient model
class Patient(Timestamped):
    name = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    disease = models.CharField(max_length=200, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='patients')

    def __str__(self):
        return self.name

# 🩺 Doctor model
class Doctor(Timestamped):
    name = models.CharField(max_length=100)
    specialization = models.CharField(max_length=120)

    def __str__(self):
        return f"{self.name} ({self.specialization})"

# 🧑‍⚕️ Patient ↔ Doctor mapping
class PatientDoctor(Timestamped):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='doctor_links')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='patient_links')

    class Meta:
        unique_together = ('patient', 'doctor')

class UserProfile(models.Model):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('patient', 'Patient'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='patient')

    def __str__(self):
        return f"{self.user.username} - {self.role}"

# 🔔 Automatically create UserProfile whenever a new User is created
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
