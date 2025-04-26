from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from rest_framework import status, viewsets, mixins
from rest_framework.decorators import (
    action,
    api_view,
    permission_classes
)
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from api_yamdb.constants import EMAIL_ADRES
from .models import User
from .mixins import PatchModelMixin
from .serializers import (
    SignupSerializer,
    TokenSerializer,
    UserSerializer
)
from .permissions import IsAdmin


@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    serializer = SignupSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.save()
    confirmation_code = default_token_generator.make_token(user)
    send_mail(
        'Код подтверждения YaMDB',
        f'Ваш код: {confirmation_code}',
        EMAIL_ADRES,
        [user.email],
        fail_silently=False
    )
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def get_token(request):
    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.validated_data['user']
    if default_token_generator.check_token(
        user,
        serializer.validated_data['confirmation_code']
    ):
        token = AccessToken.for_user(user)
        return Response(
            {'token': str(token)},
            status=status.HTTP_200_OK
        )
    return Response(
        {'error': 'Неверный код подтверждения'},
        status=status.HTTP_400_BAD_REQUEST
    )


class UserViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    PatchModelMixin,
    viewsets.GenericViewSet
):
    """
    ViewSet для управления пользователями.
    (только для администраторов).
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(
        detail=False,
        methods=['get', 'patch'],
        url_path='me',
        permission_classes=[IsAdmin]
    )
    def me(self, request):
        user = request.user

        if request.method == 'GET':
            serializer = self.get_serializer(user)
            return Response(serializer.data)

        serializer = self.get_serializer(
            user,
            data=request.data,
            partial=True,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @action(
        detail=False,
        methods=['delete'],
        url_path='me',
        permission_classes=[IsAdmin]
    )
    def delete_me(self, request):
        """Удаляет текущего пользователя."""
        request.user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
