from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Updated choices to include STAFF and ADMIN
    ROLE_CHOICES = [
        ('PATIENT', 'Patient'),
        ('STAFF', 'Staff'),
        ('ADMIN', 'Admin'),
        ('DOCTOR', 'Doctor'),
        ('MIDWIFE', 'Midwife'),
        ('NURSE', 'Nurse'),
    ]
    role = models.CharField(max_length=15, choices=ROLE_CHOICES, default='PATIENT')
    
    # Added approval flag for Staff workflow
    is_approved = models.BooleanField(default=False)

    # Link patients to their primary clinician once claimed
    assigned_staff = models.ForeignKey(
        'self', on_delete=models.SET_NULL, null=True, blank=True, related_name='patients'
    )

class PatientProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='patient_profile')
    estimated_due_date = models.DateField(null=True, blank=True)
    current_week = models.IntegerField(null=True, blank=True)
    emergency_contact_name = models.CharField(max_length=255, blank=True)
    emergency_contact_phone = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Profile of {self.user.username}"

class HealthLog(models.Model):
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='account_health_logs')
    weight = models.FloatField()
    blood_pressure = models.CharField(max_length=20)
    kick_count = models.IntegerField(null=True, blank=True)
    symptoms = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

class Appointment(models.Model):
    STATUS_CHOICES = [('REQUESTED', 'Requested'), ('SCHEDULED', 'Scheduled'), ('COMPLETED', 'Completed')]
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='account_appointments')
    assigned_staff = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='account_staff_appointments')
    agenda = models.CharField(max_length=255)
    date = models.DateField(null=True, blank=True)
    time = models.TimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='REQUESTED')

class ClinicalNote(models.Model):
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='account_clinical_notes')
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='account_authored_notes')
    notes = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)