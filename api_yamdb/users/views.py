# users/views.py
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken
from reviews.models import CustomUser
from .serializers import SignupSerializer, TokenSerializer, UserSerializer, MeSerializer
from .permissions import IsAdmin

@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    serializer = SignupSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user, _ = CustomUser.objects.get_or_create(
        username=serializer.validated_data['username'],
        email=serializer.validated_data['email']
    )
    confirmation_code = default_token_generator.make_token(user)
    send_mail(
        'Код подтверждения YaMDB',
        f'Ваш код: {confirmation_code}',
        'noreply@yamdb.fake',
        [user.email],
        fail_silently=False
    )
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([AllowAny])
def get_token(request):
    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = get_object_or_404(CustomUser, username=serializer.validated_data['username'])
    if default_token_generator.check_token(user, serializer.validated_data['confirmation_code']):
        token = AccessToken.for_user(user)
        return Response({'token': str(token)}, status=status.HTTP_200_OK)
    return Response({'error': 'Неверный код подтверждения'}, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsAdmin]
    lookup_field = 'username'

    @action(detail=False, methods=['get', 'patch'], permission_classes=[IsAuthenticated])
    def me(self, request):
        user = request.user
        if request.method == 'PATCH':
            serializer = MeSerializer(user, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        serializer = MeSerializer(user)
        return Response(serializer.data)
