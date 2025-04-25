from django.core.validators import RegexValidator
from rest_framework import serializers

from .models import User
from api_yamdb.constants import (
    EMAIL_MAX_LENGTH,
    USERNAME_MAX_LENGTH
)


class SignupSerializer(serializers.Serializer):
    """Сериализатор для регистрации нового пользователя."""

    email = serializers.EmailField(
        max_length=EMAIL_MAX_LENGTH
    )
    username = serializers.CharField(
        max_length=150,
        validators=[
            RegexValidator(
                regex=r"^[a-zA-Z0-9_.@+-]+\Z",
                message='Никнейм может содержать только символы @/./+/-/_',
                code='invalid_username'
            )
        ]
    )

    def validate(self, data):
        """Проверяет, что имя пользователя не 'me'."""
        if data['username'].lower() == 'me':
            raise serializers.ValidationError(
                "Username 'me' запрещен."
            )
        return data


class TokenSerializer(serializers.Serializer):
    """Сериализатор для получения JWT-токена."""

    username = serializers.CharField(
        max_length=USERNAME_MAX_LENGTH
    )
    confirmation_code = serializers.CharField()


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


class MeSerializer(serializers.ModelSerializer):
    """Сериализатор для текущего пользователя."""

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
        read_only_fields = ('role',)
