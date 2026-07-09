from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import PregnancyProfile, HealthLog

User = get_user_model()


class PregnancyProfileSerializer(serializers.ModelSerializer):
    patient_username = serializers.ReadOnlyField(source='patient.username')
    patient_id = serializers.ReadOnlyField(source='patient.id')
    patient = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False)

    class Meta:
        model = PregnancyProfile
        fields = [
            'id', 'patient', 'patient_id', 'patient_username',
            'full_name', 'age', 'phone', 'address',
            'emergency_contact_name', 'emergency_contact_phone',
            'last_menstrual_period_date', 'current_week', 'estimated_due_date',
            'blood_group', 'existing_conditions', 'allergies',
            'medical_history_notes', 'is_profile_complete',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'estimated_due_date', 'is_profile_complete', 'created_at', 'updated_at']


class HealthLogSerializer(serializers.ModelSerializer):
    patient_username = serializers.ReadOnlyField(source='patient.username')
    patient = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False)

    class Meta:
        model = HealthLog
        fields = [
            'id', 'patient', 'patient_username', 'recorded_at',
            'weight_kg', 'blood_pressure', 'temperature',
            'fetal_kick_count', 'symptom', 'symptom_other',
            'mood', 'urgent_attention_requested'
        ]
        read_only_fields = ['id', 'recorded_at']

    def validate(self, data):
        if data.get('symptom') == 'OTHER' and not data.get('symptom_other'):
            raise serializers.ValidationError(
                {'symptom_other': 'Please describe your symptom when selecting Other.'}
            )
        return data