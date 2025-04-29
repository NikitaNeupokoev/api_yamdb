from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail

from rest_framework import (
    mixins,
    viewsets,
    filters,
    status
)
from rest_framework.decorators import (
    api_view,
    permission_classes,
    action
)
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated
)
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from users.models import User

from api_yamdb.constants import EMAIL_ADRES
from api.v1.mixins import PatchModelMixin
from api.v1.permissions import IsAdmin
from .serializers import (
    SignupSerializer,
    TokenSerializer,
    UserSerializer
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
    (только для админов).
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdmin]
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    lookup_field = 'username'

    @action(
        detail=False,
        methods=['get'],
        permission_classes=[IsAuthenticated]
    )
    def me(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)

    @me.mapping.patch
    def patch_me(self, request):
        user = request.user
        serializer = UserSerializer(
            user,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(role=user.role)
        return Response(serializer.data)
