from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

from .models import Vendor

User = get_user_model()


class UserRegistrationSerializer(serializers.ModelSerializer):
    # Serializer for user registration
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password]
    )
    password2 = serializers.CharField(
        write_only=True,
        required=True,
        label="Confirm Password"
    )

    class Meta:
        model = User
        fields = ('email', 'username', 'password', 'password2', 'first_name', 'last_name')
        extra_kwargs = {
            'first_name': {'required': False},
            'last_name': {'required': False},
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."}
            )
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        return user


class UserSerializer(serializers.ModelSerializer):
    # Serializer for user information
    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'first_name', 'last_name', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at')


class VendorListSerializer(serializers.ModelSerializer):
    # Serializer for vendor list view (minimal fields)
    class Meta:
        model = Vendor
        fields = ('id', 'vendor_name', 'phone_number', 'email_address', 'primary_contact_name', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at')


class VendorDetailSerializer(serializers.ModelSerializer):
    # Serializer for vendor detail view (all fields)
    class Meta:
        model = Vendor
        fields = (
            'id',
            'vendor_name',
            'address',
            'phone_number',
            'email_address',
            'website',
            'primary_contact_name',
            'created_at',
            'updated_at'
        )
        read_only_fields = ('id', 'created_at', 'updated_at')

