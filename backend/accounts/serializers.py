from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'role']


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, validators=[validate_password]
    )

    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'password', 'role']

    def validate_email(self, value):
        value = value.lower()
        if len(value) > 150:
            raise serializers.ValidationError('Email is too long.')
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError('This email is already registered.')
        return value

    def validate_role(self, value):
        if value == User.Role.ADMIN:
            raise serializers.ValidationError(
                'Admin accounts cannot be created through registration.'
            )
        return value

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(username=validated_data['email'], **validated_data)
        user.set_password(password)
        user.save()
        return user


class EmailTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Log in with email + password instead of username."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.pop('username')
        self.fields['email'] = serializers.EmailField()

    def validate(self, attrs):
        attrs['username'] = attrs.pop('email').lower()
        data = super().validate(attrs)
        data['user'] = UserSerializer(self.user).data
        return data