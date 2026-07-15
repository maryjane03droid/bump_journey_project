from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Appointment, StaffNote, AuditTrail

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role']


class AppointmentSerializer(serializers.ModelSerializer):
    doctor_username = serializers.ReadOnlyField(source='doctor.username')
    patient_username = serializers.ReadOnlyField(source='patient.username')
    locked_by_username = serializers.ReadOnlyField(source='locked_by.username')
    referred_by_username = serializers.ReadOnlyField(source='referred_by.username')
    referred_to_username = serializers.ReadOnlyField(source='referred_to.username')
    patient = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False)
    doctor = serializers.PrimaryKeyRelatedField(read_only=True)
    status = serializers.CharField(read_only=False)

    class Meta:
        model = Appointment
        fields = [
            'id', 'patient', 'patient_username',
            'doctor', 'doctor_username',
            'date', 'time', 'reason', 'status',
            'is_locked', 'locked_by', 'locked_by_username',
            'referred_by', 'referred_by_username',
            'referred_to', 'referred_to_username',
            'created_at', 'updated_at'
        ]
        extra_kwargs = {
            'date': {'required': False},
            'time': {'required': False},
            'reason': {'required': False},
            'is_locked': {'read_only': True},
            'locked_by': {'read_only': True},
            'referred_by': {'read_only': True},
            'referred_to': {'read_only': True},
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
            'id', 'patient', 'patient_username',
            'author', 'author_username',
            'appointment', 'notes', 'prescriptions', 'created_at'
        ]
        extra_kwargs = {
            'author': {'read_only': True}
        }


class AuditTrailSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source='user.username')
    patient_username = serializers.ReadOnlyField(source='patient.username')

    class Meta:
        model = AuditTrail
        fields = [
            'id', 'user', 'username', 'user_role', 'action',
            'patient', 'patient_username', 'description',
            'old_value', 'new_value', 'created_at'
        ]
