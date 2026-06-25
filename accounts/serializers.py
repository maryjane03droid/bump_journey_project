from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import PatientProfile

User = get_user_model()

# 1. REGISTER SERIALIZER (Base margin)
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'role']

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create(**validated_data)
        user.set_password(password)  # Hashes the password securely
        user.save()
        return user


# 2. PATIENT PROFILE SERIALIZER (Moved to base margin)
class PatientProfileSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source='user.username')
    email = serializers.ReadOnlyField(source='user.email')

    class Meta:
        model = PatientProfile
        fields = [
            'id', 
            'username', 
            'email', 
            'estimated_due_date', 
            'current_week', 
            'emergency_contact_name', 
            'emergency_contact_phone'
        ]