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
        # Auto-approve patients upon registration; staff/admins require approval
        if self.role == 'PATIENT':
            self.is_approved = True
        super().save(*args, **kwargs)