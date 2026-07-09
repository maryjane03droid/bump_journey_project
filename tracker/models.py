from django.db import models
from django.conf import settings
from datetime import timedelta


class PregnancyProfile(models.Model):
    patient = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='pregnancy_profile')
    full_name = models.CharField(max_length=255)
    age = models.IntegerField()
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=255)
    emergency_contact_name = models.CharField(max_length=255)
    emergency_contact_phone = models.CharField(max_length=20)
    last_menstrual_period_date = models.DateField()
    current_week = models.IntegerField(help_text='How many weeks pregnant currently')
    estimated_due_date = models.DateField(blank=True, null=True)
    blood_group = models.CharField(max_length=10)
    existing_conditions = models.TextField(blank=True, null=True)
    allergies = models.TextField(blank=True, null=True)
    medical_history_notes = models.TextField(blank=True, null=True)
    is_profile_complete = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.last_menstrual_period_date and not self.estimated_due_date:
            self.estimated_due_date = self.last_menstrual_period_date + timedelta(days=280)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Profile for {self.patient.username}"


class HealthLog(models.Model):
    SYMPTOM_CHOICES = [
        ('NAUSEA', 'Nausea/Morning Sickness'),
        ('BACK_PAIN', 'Back Pain'),
        ('SWOLLEN_FEET', 'Swollen Feet'),
        ('HEADACHE', 'Headache'),
        ('FATIGUE', 'Fatigue'),
        ('DIZZINESS', 'Dizziness'),
        ('HEARTBURN', 'Heartburn'),
        ('CONSTIPATION', 'Constipation'),
        ('CRAMPING', 'Cramping'),
        ('SHORTNESS_OF_BREATH', 'Shortness of Breath'),
        ('INSOMNIA', 'Insomnia'),
        ('FREQUENT_URINATION', 'Frequent Urination'),
        ('OTHER', 'Other'),
    ]

    MOOD_CHOICES = [
        ('HAPPY', 'Happy'),
        ('SAD', 'Sad'),
        ('TIRED', 'Tired'),
        ('STRESSED', 'Stressed'),
    ]

    patient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='health_logs')
    recorded_at = models.DateTimeField(auto_now_add=True)
    weight_kg = models.DecimalField(max_digits=5, decimal_places=2)
    blood_pressure = models.CharField(max_length=20, help_text='Format: 120/80')
    temperature = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True, help_text='In Celsius')
    fetal_kick_count = models.IntegerField(blank=True, null=True)
    symptom = models.CharField(max_length=25, choices=SYMPTOM_CHOICES, blank=True, null=True)
    symptom_other = models.TextField(blank=True, null=True, help_text='Describe if symptom is Other')
    mood = models.CharField(max_length=10, choices=MOOD_CHOICES, blank=True, null=True)
    urgent_attention_requested = models.BooleanField(default=False)

    class Meta:
        ordering = ['-recorded_at']

    def __str__(self):
        return f"HealthLog for {self.patient.username} - {self.recorded_at.date()}"