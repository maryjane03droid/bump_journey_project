from rest_framework import serializers
from .models import SymptomLog

class SymptomLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = SymptomLog
        fields = ['id', 'symptom_name', 'severity', 'notes', 'logged_at']
        read_only_fields = ['id', 'logged_at']