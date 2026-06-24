from rest_framework import serializers
from .models import Appointment, StaffNote

class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ['id', 'patient', 'date', 'time', 'reason', 'status', 'created_at']

class StaffNoteSerializer(serializers.ModelSerializer):
    # This allows Postman to send notes with OR without an appointment ID
    appointment = serializers.PrimaryKeyRelatedField(
        required=False, 
        allow_null=True, 
        queryset=Appointment.objects.all()
    )

    class Meta:
        model = StaffNote
        fields = ['id', 'patient', 'appointment', 'notes', 'prescriptions', 'created_at']