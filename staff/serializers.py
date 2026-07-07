from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Appointment, StaffNote

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role']


class AppointmentSerializer(serializers.ModelSerializer):
    doctor_username = serializers.ReadOnlyField(source='doctor.username')
    patient_username = serializers.ReadOnlyField(source='patient.username')
    patient = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    doctor = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Appointment
        fields = [
            'id', 'patient', 'patient_username', 'doctor',
            'doctor_username', 'date', 'time', 'reason', 'status', 'created_at'
        ]
        extra_kwargs = {
            'doctor': {'read_only': True},
        }

class StaffNoteSerializer(serializers.ModelSerializer):
    author_username = serializers.ReadOnlyField(source='author.username')
    patient_username = serializers.ReadOnlyField(source='patient.username') 
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
            'author': {'read_only': True} 
        }