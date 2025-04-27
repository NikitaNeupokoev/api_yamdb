from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets, mixins 
from rest_framework.decorators import (
    action,
    api_view,
    permission_classes
)
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated
)
from rest_framework.response import Response
from rest_framework import filters
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.exceptions import MethodNotAllowed


from users.models import User

from .serializers import (
    SignupSerializer,
    TokenSerializer,
    UserSerializer
)
from .permissions import IsAdmin
from api_yamdb.constants import EMAIL_ADRES


@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    serializer = SignupSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data['username']
    email = serializer.validated_data['email']
    user_by_username = User.objects.filter(username=username).first()
    user_by_email = User.objects.filter(email=email).first()
    if user_by_username:
        if user_by_username.email != email:
            return Response(
                {"error": "Пользователь с таким username уже существует"},
                status=status.HTTP_400_BAD_REQUEST
            )
        user = user_by_username
    else:
        if user_by_email:
            return Response(
                {"error": "Пользователь с таким email уже существует"},
                status=status.HTTP_400_BAD_REQUEST
            )
        user = User.objects.create(username=username, email=email)
    confirmation_code = default_token_generator.make_token(user)
    send_mail(
        'Код подтверждения YaMDB',
        f'Ваш код: {confirmation_code}',
        EMAIL_ADRES,
        [user.email],
        fail_silently=False
    )
    return Response(
        serializer.data,
        status=status.HTTP_200_OK
    )


@api_view(['POST'])
@permission_classes([AllowAny])
def get_token(request):
    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.validated_data['user']
    token = AccessToken.for_user(user)
    return Response({'token': str(token)}, status=status.HTTP_200_OK)


class UserViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    """
    ViewSet для управления пользователями (только для админов).
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdmin]
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    lookup_field = 'username'

    @action(detail=False, methods=['get', 'patch'], permission_classes=[IsAuthenticated])
    def me(self, request):
        user = request.user
        if request.method == 'PATCH':
            serializer = UserSerializer(
                user,
                data=request.data,
                partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save(role=user.role)
            return Response(serializer.data)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=200)

