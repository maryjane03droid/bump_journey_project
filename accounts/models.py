from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = [
        ('PATIENT', 'Patient'),
        ('STAFF', 'Staff'),
        ('ADMIN', 'Admin'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='PATIENT')
    is_approved = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        # Patients are auto-approved to clear onboarding friction; staff/admins require verification
        if self.role == 'PATIENT':
            self.is_approved = True
        super().save(*args, **kwargs)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    full_name = models.CharField(max_length=255, blank=True, default='')
    due_date = models.DateField(null=True, blank=True)
    bio = models.TextField(blank=True, default='')

    def __str__(self):
        return f"Profile for {self.user.username}"