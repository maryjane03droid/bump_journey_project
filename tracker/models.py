from django.db import models
from django.conf import settings
from datetime import timedelta

class PregnancyProfile(models.Model):
    patient = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='pregnancy_profile')
    last_menstrual_period_date = models.DateField()
    estimated_due_date = models.DateField(blank=True, null=True)
    blood_group = models.CharField(max_length=10)
    medical_history_notes = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        # Auto-calculates EDD when LMP is provided
        if self.last_menstrual_period_date and not self.estimated_due_date:
            self.estimated_due_date = self.last_menstrual_period_date + timedelta(days=280)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Profile for {self.patient.username}"


class HealthLog(models.Model):
    patient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='health_logs')
    recorded_at = models.DateTimeField(auto_now_add=True)
    weight_kg = models.DecimalField(max_digits=5, decimal_places=2)
    blood_pressure = models.CharField(max_length=20, help_text="Format: 120/80")
    fetal_kick_count = models.IntegerField(blank=True, null=True)
    symptoms = models.TextField(blank=True, null=True)
    
    # NEW: Allows the patient to flag a daily log as urgent for the doctor's dashboard
    urgent_attention_requested = models.BooleanField(default=False)

    class Meta:
        ordering = ['-recorded_at']

    def __str__(self):
        return f"HealthLog for {self.patient.username} - {self.recorded_at.date()}"