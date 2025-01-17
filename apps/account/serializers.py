from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True, required=True, min_length=8)

    class Meta:
        model = User
        fields = ('email', 'password', 'password_confirm', 'first_name', 'last_name')

    def validate(self, attrs):
        password = attrs.get('password')
        password_confirm = attrs.pop('password_confirm')

        if password != password_confirm:
            raise serializers.ValidationError('Passwords do not match')
        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class LogoutSerializer(serializers.Serializer):
    refresh_token = serializers.CharField(required=True, write_only=True)


class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

class ResetPasswordConfirmSerializer(serializers.Serializer):
    code = serializers.CharField(required=True, max_length=6)
    password = serializers.CharField(required=True, write_only=True, min_length=8)
    password_confirm = serializers.CharField(required=True, write_only=True, min_length=8)

    def validate(self, attrs):
        password = attrs.get('password')
        password_confirm = attrs.pop('password_confirm')

        if password != password_confirm:
            raise serializers.ValidationError('Passwords do not match')
        return attrs