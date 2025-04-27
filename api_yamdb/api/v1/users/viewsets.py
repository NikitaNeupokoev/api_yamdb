from rest_framework import viewsets, mixins 
from rest_framework.decorators import (
    action,
)
from rest_framework.permissions import (
    IsAuthenticated
)
from rest_framework.response import Response
from rest_framework import filters


from users.models import User
from .serializers import (
    UserSerializer
)
from .permissions import IsAdmin

class UserViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
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

    def update(self, request, *args, **kwargs):
        if request.method == 'PUT':
            return Response(status=405)
        return super().update(request, *args, **kwargs)

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
        return Response(serializer.data)

