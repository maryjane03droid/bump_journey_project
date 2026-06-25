from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class VitalLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='vital_logs')
    weight = models.DecimalField(max_digits=5, decimal_places=2)
    bp = models.CharField(max_length=20) # Encodes values like "120/80"
    created_at = models.DateTimeField(auto_now_add=True)

class SymptomLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='symptom_logs')
    symptom_name = models.CharField(max_length=255)
    severity = models.CharField(max_length=50) # Low, Medium, High
    notes = models.TextField(blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)

class ClinicalNote(models.Model):
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='clinical_notes_received')
    provider = models.ForeignKey(User, on_delete=models.CASCADE, related_name='clinical_notes_authored')
    notes = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)