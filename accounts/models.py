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

    # Staff approval workflow: staff cannot login until admin approves
    is_approved = models.BooleanField(default=False)

    # License number for staff (10 digits, numbers only)
    license_number = models.CharField(max_length=10, blank=True, null=True)

    # Link patients to their primary clinician
    assigned_staff = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='patients'
    )

    # Helper properties
    @property
    def is_primary_staff(self):
        """Doctors, Pediatricians, and Nurses can attend patients directly."""
        return self.role in ['DOCTOR', 'PEDIATRICIAN', 'NURSE']

    @property
    def is_specialist_staff(self):
        """Midwives, Nutritionists, Lab Techs, Therapists only receive referrals."""
        return self.role in ['MIDWIFE', 'NUTRITIONIST', 'LAB_TECHNICIAN', 'THERAPIST']

    @property
    def is_any_staff(self):
        """Any staff role (primary or specialist)."""
        return self.is_primary_staff or self.is_specialist_staff

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"