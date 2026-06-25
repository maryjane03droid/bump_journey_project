from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Profile

User = get_user_model()

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['full_name', 'due_date', 'bio']

class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'email', 'role', 'is_approved', 'date_joined', 'profile']
        extra_kwargs = {
            'password': {'write_only': True},
            'is_approved': {'read_only': True}
        }

    def create(self, validated_data):
        role = validated_data.get('role', 'PATIENT')
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data.get('email', ''),
            role=role
        )
        # Instantiate a corresponding empty profile immediately
        Profile.objects.create(user=user)
        return user