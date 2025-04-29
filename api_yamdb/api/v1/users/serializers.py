from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from api.v1.mixins import UsernameValidatorMixin
from api_yamdb.constants import (
    EMAIL_MAX_LENGTH,
    USERNAME_MAX_LENGTH
)
from django.contrib.auth.tokens import default_token_generator

User = get_user_model()


class SignupSerializer(
    UsernameValidatorMixin,
    serializers.Serializer
):
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
        """
        Проверяет, что пользователь с таким
        username/email не существует.
        """
        username = data['username']
        email = data['email']

        user_by_username = User.objects.filter(username=username).first()
        user_by_email = User.objects.filter(email=email).first()

        if user_by_username and user_by_username.email != email:
            raise serializers.ValidationError(
                "Пользователь с таким username уже существует"
            )
        if user_by_email and user_by_email.username != username:
            raise serializers.ValidationError(
                "Пользователь с таким email уже существует"
            )

        return data

    def save(self):
        """Создает или возвращает существующего пользователя."""
        username = self.validated_data['username']
        email = self.validated_data['email']

        user, created = User.objects.get_or_create(
            username=username,
            defaults={'email': email}
        )
        if not created and user.email != email:
            user.email = email
            user.save()
        return user


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=USERNAME_MAX_LENGTH)
    confirmation_code = serializers.CharField()

    def validate(self, data):
        """Проверяет username и confirmation_code."""
        username = data['username']
        confirmation_code = data['confirmation_code']

        user = get_object_or_404(User, username=username)

        if not default_token_generator.check_token(
            user,
            confirmation_code
        ):
            raise serializers.ValidationError(
                'Неверный код подтверждения'
            )

        data['user'] = user
        return data


class UserSerializer(
    UsernameValidatorMixin,
    serializers.ModelSerializer
):
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
