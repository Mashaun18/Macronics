from requests import Response
from rest_framework import serializers, status
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import Userr
from django.core.validators import EmailValidator
from django.db import models


class UserRole(models.TextChoices):
    ADMIN = 'admin', 'admin'
    VENDOR = 'vendor', 'vendor'
    CUSTOMER = 'customer', 'customer'


class CustomTokenObtainPairView(TokenObtainPairView):
    def validate(self, attrs):
        data = super().validate(attrs)
        print("Validated Data:", data)
        user = self.user
        if not user.is_active:
            print("User is inactive")
            raise serializers.ValidationError({"detail": "User account is disabled."})
        if not user.user_type or user.user_type not in [role.value for role in UserRole]:
            print("Invalid user type")
            raise serializers.ValidationError({"detail": "User does not have a valid role"})
        data['user_type'] = user.user_type
        return data


class UserSerializer(serializers.ModelSerializer):
    user_data = serializers.SerializerMethodField()

    class Meta:
        model = Userr
        fields = ['id', 'username', 'email', 'user_type', 'first_name', 'last_name', 'is_active', 'user_data']

    def get_user_data(self, obj):
        user = obj
        return {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'user_type': user.user_type,
        }

class UserSignupSerializer(serializers.ModelSerializer):
    user_type = serializers.ChoiceField(choices=UserRole.choices)
    user = serializers.CharField()

    class Meta:
        model = Userr
        fields = ['username', 'password', 'email', 'user_type', 'first_name', 'last_name']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        print(validated_data)
        user = Userr.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data['email'],
            user_type=validated_data['user_type'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        return user

    def validate_user(self, value):
        try:
            if value.isdigit():
                return Userr.objects.get(pk=value)  # Fetch user by primary key
            else:
                return Userr.objects.get(username=value)  # Fetch user by username
        except Userr.DoesNotExist:
            raise serializers.ValidationError("User does not exist.")

    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError('Password must be at least 8 characters long')
        if not any(char.isdigit() for char in value):
            raise serializers.ValidationError('Password must contain at least one digit')
        if not any(char.isalpha() for char in value):
            raise serializers.ValidationError('Password must contain at least one letter')
        return value

    def validate_email(self, value):
        email_validator = EmailValidator()
        try:
            email_validator(value)
        except serializers.ValidationError:
            raise serializers.ValidationError("Invalid email address")
        return value

    def validate_username(self, value):
        if Userr.objects.filter(username=value).exists():
            raise serializers.ValidationError('Username already exists')
        return value