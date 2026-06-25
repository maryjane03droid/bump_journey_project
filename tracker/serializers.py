from rest_framework import serializers
from .models import VitalLog, SymptomLog, ClinicalNote

class VitalLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = VitalLog
        fields = ['id', 'weight', 'bp', 'created_at']

class SymptomLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = SymptomLog
        fields = ['id', 'symptom_name', 'severity', 'notes', 'created_at']

class ClinicalNoteSerializer(serializers.ModelSerializer):
    provider_name = serializers.CharField(source='provider.username', read_only=True)

    class Meta:
        model = ClinicalNote
        fields = ['id', 'patient', 'provider_name', 'notes', 'created_at']