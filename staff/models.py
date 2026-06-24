from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Appointment(models.Model):
    STATUS_CHOICES = [
        ('SCHEDULED', 'Scheduled'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    ]

    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='appointments')
    date = models.DateField()
    time = models.TimeField()
    reason = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='SCHEDULED')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date', '-time']

    def __str__(self):
        return f"{self.patient.username} - {self.date} at {self.time}"


class StaffNote(models.Model):
    # Direct one-to-many relationship with the Patient's account
    patient = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name="staff_notes"
    )
    
    # Decoupled relationship: optional field allowing null database values
    appointment = models.ForeignKey(
        'Appointment',  # This now perfectly links to the class above!
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name="notes"
    )
    
    notes = models.TextField()
    prescriptions = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Note for {self.patient.username} on {self.created_at.strftime('%Y-%m-%d')}"