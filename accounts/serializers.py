from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer  # <-- Add this import
from .models import PatientProfile

User = get_user_model()

# --- ADD THIS CLASS ---
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        # Include custom user fields in the JSON response
        data['username'] = self.user.username
        data['role'] = self.user.role
        return data

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'role']
        extra_kwargs = {
            'role': {'required': False, 'default': 'PATIENT'},
            'email': {'required': False, 'allow_blank': True}
        }
        
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user

class PatientProfileSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source='user.username')
    email = serializers.ReadOnlyField(source='user.email')

    class Meta:
        model = PatientProfile
        fields = [
            'id', 
            'username', 
            'email', \
            'estimated_due_date', 
            'current_week', 
            'emergency_contact_name', 
            'emergency_contact_phone'
        ]