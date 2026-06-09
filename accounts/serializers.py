from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = User
        # Include username/email, password, and your custom required role field
        fields = ['id', 'username', 'email', 'password', 'role']

    def create(self, validated_data):
        # Safely extract password and create a user with a properly hashed password
        password = validated_data.pop('password')
        user = User.objects.create(**validated_data)
        user.set_password(password)  # Hashes the password securely
        user.save()
        return user