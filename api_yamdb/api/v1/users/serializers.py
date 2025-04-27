from rest_framework import serializers
from django.core.validators import RegexValidator
from django.shortcuts import get_object_or_404
from django.contrib.auth.tokens import default_token_generator  

from users.models import User
from api_yamdb.constants import EMAIL_MAX_LENGTH, USERNAME_MAX_LENGTH


class SignupSerializer(serializers.Serializer):
    """Сериализатор для регистрации нового пользователя."""

    email = serializers.EmailField(max_length=EMAIL_MAX_LENGTH)
    username = serializers.CharField(
        max_length=USERNAME_MAX_LENGTH,
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
    username = serializers.CharField(max_length=USERNAME_MAX_LENGTH)
    confirmation_code = serializers.CharField()

    def validate(self, data):
        username = data['username']
        confirmation_code = data['confirmation_code']
        user = get_object_or_404(User, username=username)
        if not default_token_generator.check_token(user, confirmation_code):
            raise serializers.ValidationError('Неверный код подтверждения')
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
    def validate_username(self, value):
        if value.lower() == 'me':
            raise serializers.ValidationError('Имя "me" запрещено для использования.')
        return value
