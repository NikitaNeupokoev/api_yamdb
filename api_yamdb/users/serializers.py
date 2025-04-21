from rest_framework import serializers

from reviews.models import CustomUser


class SignupSerializer(serializers.Serializer):
    """Сериализатор для регистрации нового пользователя."""

    email = serializers.EmailField()
    username = serializers.CharField(max_length=150)

    def validate(self, data):
        """Проверяет, что имя пользователя не 'me'."""
        if data['username'].lower() == 'me':
            raise serializers.ValidationError(
                "Username 'me' запрещен."
            )
        return data


class TokenSerializer(serializers.Serializer):
    """Сериализатор для получения JWT-токена."""

    username = serializers.CharField(max_length=150)
    confirmation_code = serializers.CharField()


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для пользователей (для администраторов)."""

    class Meta:
        model = CustomUser
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
        model = CustomUser
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
        )
        read_only_fields = ('role',)
