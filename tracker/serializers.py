from rest_framework import serializers
from .models import PregnancyProfile, HealthLog

class PregnancyProfileSerializer(serializers.ModelSerializer):
    patient_username = serializers.ReadOnlyField(source='patient.username')
    
    class Meta:
        model = PregnancyProfile
        fields = ['id', 'patient', 'patient_username', 'last_menstrual_period_date', 'estimated_due_date', 'blood_group', 'medical_history_notes']
        read_only_fields = ['id', 'estimated_due_date']

class HealthLogSerializer(serializers.ModelSerializer):
    patient_username = serializers.ReadOnlyField(source='patient.username')

    class Meta:
        model = HealthLog
        # ADDED: 'urgent_attention_requested' to the fields list
        fields = ['id', 'patient', 'patient_username', 'recorded_at', 'weight_kg', 'blood_pressure', 'fetal_kick_count', 'symptoms', 'urgent_attention_requested']
        read_only_fields = ['id', 'recorded_at']