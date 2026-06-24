from rest_framework import serializers
from .models import Appointment, ClinicalNote

class AppointmentSerializer(serializers.ModelSerializer):
    patient_username = serializers.ReadOnlyField(source='patient.username')
    doctor_username = serializers.ReadOnlyField(source='doctor.username')

    class Meta:
        model = Appointment
        fields = ['id', 'patient', 'patient_username', 'doctor', 'doctor_username', 'appointment_date', 'status', 'reason_for_visit']
        read_only_fields = ['id']

class ClinicalNoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClinicalNote
        fields = ['id', 'appointment', 'notes', 'prescriptions', 'created_at']
        read_only_fields = ['id', 'created_at']