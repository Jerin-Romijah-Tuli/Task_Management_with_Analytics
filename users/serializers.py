from rest_framework import serializers
from .models import User, PasswordReset
from django.contrib.auth import authenticate
from django.utils import timezone
from datetime import timedelta

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            name=validated_data['name'],
            password=validated_data['password'],
            address=validated_data['address'],
            mobile_number=validated_data['mobile_number'],
            date_of_birth=validated_data['date_of_birth'],
            username= validated_data['username'],
            
        )
        return user

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')
        if email and password:
            user = authenticate(request=self.context.get('request'), email=email, password=password)
            if not user:
                raise serializers.ValidationError("Invalid login credentials")
        else:
            raise serializers.ValidationError("Must include 'email' and 'password'")
        data['user'] = user
        return data

class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        try:
            user = User.objects.get(email=value)
        except User.DoesNotExist:
            raise serializers.ValidationError("User with this email does not exist")
        return value

class PasswordResetConfirmSerializer(serializers.Serializer):
    email = serializers.EmailField()
    recovery_code = serializers.CharField()
    new_password = serializers.CharField()

    def validate(self, data):
        try:
            user = User.objects.get(email=data['email'])
            reset = PasswordReset.objects.get(user=user, recovery_code=data['recovery_code'])
            if not reset.is_valid():
                raise serializers.ValidationError("The recovery code is expired")
        except (User.DoesNotExist, PasswordReset.DoesNotExist):
            raise serializers.ValidationError("Invalid recovery code or email")
        return data
