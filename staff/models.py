from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Appointment(models.Model):
    STATUS_CHOICES = [
        ('REQUESTED', 'Requested (Pending)'),
        ('SCHEDULED', 'Scheduled'),
        ('COMPLETED', 'Completed'),
        ('REVIEWED', 'Reviewed (Advice Sent)'), # Updated from CANCELLED
    ]

    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='appointments')
    
    doctor = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        related_name='scheduled_appointments', 
        null=True,
        blank=True
    )
    
    date = models.DateField(null=True, blank=True)
    time = models.TimeField(null=True, blank=True)
    
    reason = models.CharField(max_length=255, blank=True, null=True)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='REQUESTED')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date', '-time']

    def __str__(self):
        doctor_name = self.doctor.username if self.doctor else "No Doctor Assigned"
        date_str = self.date if self.date else "TBD"
        time_str = self.time if self.time else "TBD"
        return f"{self.patient.username} - {date_str} at {time_str} with Dr. {doctor_name}"


class StaffNote(models.Model):
    patient = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name="staff_notes"
    )
    
    author = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name="authored_notes", 
        null=True
    )
    
    appointment = models.ForeignKey(
        'Appointment',  
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
        author_name = self.author.username if self.author else "Unknown Author"
        return f"Note for {self.patient.username} by {author_name} on {self.created_at.strftime('%Y-%m-%d')}"


# NEW: The Daily Tracker model for expectant mothers
class DailyLog(models.Model):
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='daily_logs')
    date = models.DateField(auto_now_add=True)
    
    symptoms = models.TextField(help_text="Describe any symptoms, e.g., nausea, cramping, headache")
    blood_pressure = models.CharField(max_length=20, blank=True, null=True, help_text="e.g., 120/80")
    weight = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    fetal_movement = models.CharField(max_length=50, blank=True, null=True, help_text="e.g., Active, Decreased")
    
    urgent_attention_requested = models.BooleanField(default=False)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"Log for {self.patient.username} on {self.date}"