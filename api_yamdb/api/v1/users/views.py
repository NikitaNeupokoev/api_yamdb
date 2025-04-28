from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail

from rest_framework import status
from rest_framework.decorators import (
    api_view,
    permission_classes
)
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from rest_framework_simplejwt.tokens import AccessToken

from api_yamdb.constants import EMAIL_ADRES
from .serializers import (
    SignupSerializer,
    TokenSerializer
)


@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    """Регистрация нового пользователя."""
    serializer = SignupSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    confirmation_code = default_token_generator.make_token(
        serializer.save()
    )
    send_mail(
        'Код подтверждения YaMDB',
        f'Ваш код: {confirmation_code}',
        EMAIL_ADRES,
        [serializer.validated_data['email']],
        fail_silently=False,
    )

    return Response(
        serializer.data,
        status=status.HTTP_200_OK
    )


@api_view(['POST'])
@permission_classes([AllowAny])
def get_token(request):
    """Получение JWT токена для пользователя."""
    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    return Response(
        {'token': str(
            AccessToken.for_user(
                serializer.validated_data['user']
            )
        )},
        status=status.HTTP_200_OK,
    )
