from rest_framework import serializers
from django.core.validators import RegexValidator
from django.shortcuts import get_object_or_404
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model

from api_yamdb.constants import EMAIL_MAX_LENGTH, USERNAME_MAX_LENGTH
from .validators import validate

User = get_user_model()


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
        """Проверяет существование пользователя по username и email."""
        username = data['username']
        email = data['email']

        validate(username)

        user_by_username = User.objects.filter(username=username).first()
        user_by_email = User.objects.filter(email=email).first()

        if user_by_username:
            if user_by_username.email != email:
                raise serializers.ValidationError(
                    {
                        "username":
                        "Пользователь с таким username уже существует."
                    }
                )
            self.instance = user_by_username
        else:
            if user_by_email:
                raise serializers.ValidationError(
                    {"email": "Пользователь с таким email уже существует."}
                )
            self.instance = User.objects.create(username=username, email=email)

        return data

    def save(self, **kwargs):
        """Возвращает пользователя, который уже есть или был создан."""
        return self.instance


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
            raise serializers.ValidationError(
                'Имя "me" запрещено для использования.'
            )
        return value
