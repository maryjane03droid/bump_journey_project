
from django.db import models
from django.conf import settings

class SymptomLog(models.Model):
    SEVERITY_CHOICES = [
        ('MILD', 'Mild'),
        ('MODERATE', 'Moderate'),
        ('SEVERE', 'Severe'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='symptom_logs'
    )
    symptom_name = models.CharField(max_length=100)  # e.g., Nausea, Fatigue, Back Pain
    severity = models.CharField(max_length=10, choices=SEVERITY_CHOICES, default='MILD')
    notes = models.TextField(blank=True, null=True)
    logged_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-logged_at']

    def __str__(self):
        return f"{self.user.username} - {self.symptom_name} ({self.severity})"