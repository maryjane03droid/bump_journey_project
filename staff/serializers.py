from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Appointment, StaffNote

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    """
    Sends user profile data and explicit system roles back to React
    """
    role = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role']

    def get_role(self, obj):
        if obj.is_superuser:
            return 'admin'
        if obj.is_staff:
            return 'doctor'  # Can be expanded to 'midwife' if using a custom field
        return 'patient'


class AppointmentSerializer(serializers.ModelSerializer):
    # Sends readable strings to React instead of just ID numbers
    doctor_username = serializers.ReadOnlyField(source='doctor.username')
    patient_username = serializers.ReadOnlyField(source='patient.username')  # ADDED for Frontend dashboards

    class Meta:
        model = Appointment
        fields = [
            'id', 'patient', 'patient_username', 'doctor', 
            'doctor_username', 'date', 'time', 'reason', 'status', 'created_at'
        ]
        extra_kwargs = {
            'doctor': {'read_only': True}  # Populated via the view, not the JSON payload
        }


class StaffNoteSerializer(serializers.ModelSerializer):
    author_username = serializers.ReadOnlyField(source='author.username')
    patient_username = serializers.ReadOnlyField(source='patient.username')  # ADDED for Frontend dashboards
    appointment = serializers.PrimaryKeyRelatedField(
        required=False, 
        allow_null=True, 
        queryset=Appointment.objects.all()
    )

    class Meta:
        model = StaffNote
        fields = [
            'id', 'patient', 'patient_username', 'author', 
            'author_username', 'appointment', 'notes', 'prescriptions', 'created_at'
        ]
        extra_kwargs = {
            'author': {'read_only': True}  # Populated via the view, not the JSON payload
        }