from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    ROLE_CHOICES = [
        ('PATIENT', 'Patient'),
        ('DOCTOR', 'Doctor'),
        ('PEDIATRICIAN', 'Pediatrician'),
        ('NURSE', 'Nurse'),
        ('MIDWIFE', 'Midwife'),
        ('NUTRITIONIST', 'Nutritionist'),
        ('LAB_TECHNICIAN', 'Lab Technician'),
        ('THERAPIST', 'Therapist'),
        ('ADMIN', 'Admin'),
    ]

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='PATIENT')
    is_approved = models.BooleanField(default=False)
    license_number = models.CharField(max_length=10, blank=True, null=True)

    assigned_staff = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='patients'
    )

    @property
    def is_primary_staff(self):
        return self.role in ['DOCTOR', 'PEDIATRICIAN', 'NURSE']

    @property
    def is_specialist_staff(self):
        return self.role in ['MIDWIFE', 'NUTRITIONIST', 'LAB_TECHNICIAN', 'THERAPIST']

    @property
    def is_any_staff(self):
        return self.is_primary_staff or self.is_specialist_staff

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"


class CareerApplication(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    role_applied = models.CharField(max_length=20, choices=User.ROLE_CHOICES)
    qualification = models.CharField(max_length=255)
    years_of_experience = models.IntegerField()
    license_number = models.CharField(max_length=10)
    message = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.full_name} - {self.role_applied} ({self.status})"


class ContactMessage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True, null=True)
    subject = models.CharField(max_length=255)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    admin_response = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.subject}"
