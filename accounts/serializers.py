from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import CareerApplication, ContactMessage

User = get_user_model()

STAFF_ROLES = ['DOCTOR', 'PEDIATRICIAN', 'NURSE', 'MIDWIFE', 'NUTRITIONIST', 'LAB_TECHNICIAN', 'THERAPIST']


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        # Block unapproved staff from logging in
        if self.user.role in STAFF_ROLES and not self.user.is_approved:
            raise serializers.ValidationError(
                'Your registration is pending admin approval. Please wait up to 24 hours.'
            )

        # Include useful info in login response
        data['user_id'] = str(self.user.id)
        data['username'] = self.user.username
        data['email'] = self.user.email
        data['role'] = self.user.role
        data['is_approved'] = self.user.is_approved
        return data


class PatientRegisterSerializer(serializers.ModelSerializer):
    """Registration for patients (clients)."""
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create(
            role='PATIENT',
            is_approved=True,
            **validated_data
        )
        user.set_password(password)
        user.save()
        return user


class StaffRegisterSerializer(serializers.ModelSerializer):
    """Registration for staff after career application is approved."""
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    license_number = serializers.CharField(
        required=True,
        min_length=10,
        max_length=10,
        help_text='Must be exactly 10 digits.'
    )

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'role', 'license_number']

    def validate_role(self, value):
        if value not in STAFF_ROLES:
            raise serializers.ValidationError(
                f'Invalid staff role. Must be one of: {", ".join(STAFF_ROLES)}'
            )
        return value

    def validate_license_number(self, value):
        if not value.isdigit():
            raise serializers.ValidationError('License number must contain only digits.')
        if len(value) != 10:
            raise serializers.ValidationError('License number must be exactly 10 digits.')
        return value

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create(
            is_approved=False,
            **validated_data
        )
        user.set_password(password)
        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):
    """For admin views: listing and managing users."""
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role', 'is_approved', 'license_number', 'date_joined']
        read_only_fields = ['id', 'date_joined']


class AdminApproveSerializer(serializers.ModelSerializer):
    """Admin approves or rejects staff registration."""
    class Meta:
        model = User
        fields = ['id', 'username', 'role', 'is_approved']
        read_only_fields = ['id', 'username', 'role']


class CareerApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CareerApplication
        fields = [
            'id', 'full_name', 'email', 'phone', 'role_applied',
            'qualification', 'years_of_experience', 'license_number',
            'message', 'status', 'created_at'
        ]
        read_only_fields = ['id', 'status', 'created_at']

    def validate_license_number(self, value):
        if not value.isdigit() or len(value) != 10:
            raise serializers.ValidationError('License number must be exactly 10 digits.')
        return value

    def validate_role_applied(self, value):
        if value not in STAFF_ROLES:
            raise serializers.ValidationError(
                f'Must apply for a staff role: {", ".join(STAFF_ROLES)}'
            )
        return value


class ContactMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactMessage
        fields = ['id', 'name', 'email', 'phone', 'subject', 'message', 'is_read', 'admin_response', 'created_at']
        read_only_fields = ['id', 'is_read', 'admin_response', 'created_at']