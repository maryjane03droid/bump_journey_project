import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

# 1. THE USER MODEL (Base margin)
class User(AbstractUser):
    ROLE_CHOICES = (
        ('PATIENT', 'Patient'),
        ('STAFF', 'Medical Staff'),
        ('ADMIN', 'Admin'),
    )
    
    # Overriding the default ID with a secure UUID primary key
    id = models.UUIDField(
        primary_key=True, 
        default=uuid.uuid4, 
        editable=False
    )
    
    email = models.EmailField(unique=True)
    role = models.CharField(
        max_length=10, 
        choices=ROLE_CHOICES, 
        default='PATIENT'
    )
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    REQUIRED_FIELDS = ['email', 'role']

    def __str__(self):
        return f"{self.username} ({self.role})"


# 2. THE PATIENT PROFILE MODEL (Separated out on the base margin)
class PatientProfile(models.Model):
    # Links profile directly to a specific User
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='patient_profile'
    )
    estimated_due_date = models.DateField(null=True, blank=True)
    current_week = models.IntegerField(default=1)
    emergency_contact_name = models.CharField(max_length=255, blank=True)
    emergency_contact_phone = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Profile for {self.user.username}"