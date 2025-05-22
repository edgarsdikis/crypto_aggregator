from rest_framework import serializers
from .models import CustomUser

class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration that handles email-based signup with password confirmation.
    """
    # Add a confirmation password field that doesn't exist in the model
    password2 = serializers.CharField(write_only=True, required=True)
    
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True},  # Don't expose password in responses
            'id': {'read_only': True}          # ID is generated, not provided by user
        }
    
    def validate(self, attrs):
        # Ensure both passwords match before proceeding
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Passwords don't match."})
        return attrs
    
    def create(self, validated_data):
        # Remove the confirmation password since it's not needed for user creation
        validated_data.pop('password2', None)
        
        # Use the custom manager to create the user
        user = CustomUser.objects.create_user(
            username=validated_data['email'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for retrieving and updating user information.
    Doesn't expose sensitive fields and protects fields that shouldn't be modified.
    """
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'is_staff', 'date_joined']
        read_only_fields = ['id', 'is_staff', 'date_joined']  # These can't be changed via API
