from django.core.validators import RegexValidator

from rest_framework import serializers

from .models import User
from api_yamdb.constants import (
    EMAIL_MAX_LENGTH,
    USERNAME_MAX_LENGTH
)


class SignupSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=EMAIL_MAX_LENGTH)
    username = serializers.CharField(
        max_length=150,
        validators=[
            RegexValidator(
                regex=r"^[\w.@+-]+\Z",
                message="Никнейм может содержать только символы @/./+/-/_"
            )
        ]
    )

    def validate(self, data):
        username = data['username']
        email = data['email']

        existing_user = User.objects.filter(username=username).first()
        existing_email = User.objects.filter(email=email).first()

        if existing_user and existing_user.email != email:
            raise serializers.ValidationError(
                {"username": "Пользователь с таким username уже существует."}
            )
        if not existing_user and existing_email:
            raise serializers.ValidationError(
                {"email": "Пользователь с таким email уже существует."}
            )
        return data

    def save(self):
        return User.objects.get_or_create(
            username=self.validated_data['username'],
            email=self.validated_data['email']
        )[0]


class TokenSerializer(serializers.Serializer):
    """Сериализатор для получения JWT-токена."""

    username = serializers.CharField(max_length=USERNAME_MAX_LENGTH)
    confirmation_code = serializers.CharField()

    def validate(self, data):
        username = data.get('username')
        user = User.objects.filter(username=username).first()
        if not user:
            raise serializers.ValidationError(
                "Пользователь с таким username не найден"
            )
        data['user'] = user
        return data


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для пользователей (для администраторов)."""

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
        )

    def validate(self, data):
        request = self.context.get('request')
        if request and not request.user.is_admin:
            if 'role' in data:
                raise serializers.ValidationError(
                    "Изменение роли запрещено для обычных пользователей."
                )
        return data

    def update(self, instance, validated_data):
        request = self.context.get('request')
        if request and not request.user.is_admin:
            validated_data.pop('role', None)
        return super().update(instance, validated_data)
